import pandas as pd
import random
import os
from datetime import datetime, timedelta
from utils.db_manager import get_db_manager

class SchedulerEngine:
    def __init__(self):
        self.db = get_db_manager()
        # self.curriculum_file path kept just in case, but primary load is via DB
        self.curriculum_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "curriculum_map.csv")
        self.schedule_template_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schedule.csv")
        self.active_schedule_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "active_schedule.csv")
        
        # Load Curriculum via DB Manager (Syncs with Supabase/Admin Panel)
        self.curriculum = self.db.load_curriculum_map()
        
        # Fallback if DB load fails or returns empty (though db_manager handles fallback too)
        if self.curriculum.empty and os.path.exists(self.curriculum_file):
            # Fallback to direct CSV read only if DB returns nothing and file exists
            self.curriculum = pd.read_csv(self.curriculum_file)
        
        # Ensure types
        if not self.curriculum.empty:
             # Ensure active is bool
             if 'active' not in self.curriculum.columns:
                 self.curriculum['active'] = True
             self.curriculum['active'] = self.curriculum['active'].astype(bool)

    def _get_next_topics(self, count=10, custom_weights=None, topic_weights=None):
        """
        Determines the next topics to study based on mastery and weights.
        custom_weights: Dictionary like {'Mathematics': 80, 'Science': 20}
        """
        if self.curriculum.empty:
            print("Warning: Curriculum is empty.")
            return []
            
        # Filter active topics
        print(f"DEBUG: Curriculum type: {type(self.curriculum)}")
        try:
            active_topics = self.curriculum[self.curriculum['active'] == True]
            print(f"DEBUG: Active topics type: {type(active_topics)}")
            if not isinstance(active_topics, pd.DataFrame):
                print("DEBUG: Active topics is NOT a DataFrame! Converting...")
                active_topics = pd.DataFrame(active_topics)
        except Exception as e:
            print(f"DEBUG: Error filtering active topics: {e}")
            return []
            
        # Ensure importance_weight is numeric
        if 'importance_weight' in active_topics.columns:
            active_topics['importance_weight'] = pd.to_numeric(active_topics['importance_weight'], errors='coerce').fillna(1)
        
        if custom_weights:
            # Normalize weights to avoid errors
            total_custom_weight = sum(custom_weights.values())
            if total_custom_weight > 0:
                # Modifying importance_weight based on custom subject weights
                # Strategy: Multiply original importance by custom weight multiplier
                for lesson, weight in custom_weights.items():
                    # Find topics for this lesson (strip whitespace just in case)
                    mask = active_topics['lesson'].astype(str).str.strip() == lesson.strip()
                    active_topics.loc[mask, 'importance_weight'] = active_topics.loc[mask, 'importance_weight'] * (weight / 10.0)
                
                if len(custom_weights) > 0:
                    # Filter keys similarly
                    clean_keys = [k.strip() for k in custom_weights.keys()]
                    active_topics = active_topics[active_topics['lesson'].astype(str).str.strip().isin(clean_keys)]

        # 2. Apply Topic-Level Custom Weights (Override or Boost)
        # 2. Apply Topic-Level Custom Weights (Override or Boost)
        if topic_weights:
            # Create a composite key for matching: "Topic (Subtopic)"
            # Handle potential NaN values gracefully
            active_topics['ui_key'] = active_topics.apply(
                lambda x: f"{str(x['topic']).strip()} ({str(x['subtopic']).strip()})", axis=1
            )
            
            for topic_key, t_weight in topic_weights.items():
                if t_weight > 0:
                    # Strategy: 
                    # 1. Try exact match against Composite Key (Most specific)
                    # 2. Try match against simple Topic Name (Broad boost)
                    
                    # Exact Match (Subtopic level)
                    mask_exact = active_topics['ui_key'] == topic_key
                    
                    # Topic Level Match (Fallback if user somehow sent just topic name, or for broad topics)
                    mask_topic = active_topics['topic'] == topic_key
                    
                    # Apply boost to whichever matches (Priority to Exact)
                    if mask_exact.any():
                        active_topics.loc[mask_exact, 'importance_weight'] = active_topics.loc[mask_exact, 'importance_weight'] * (t_weight / 20.0)
                    elif mask_topic.any():
                        active_topics.loc[mask_topic, 'importance_weight'] = active_topics.loc[mask_topic, 'importance_weight'] * (t_weight / 20.0)

        # Remove rows with 0 weight to strictly respect "0" slider (e.g. Ignore Din Kültürü if 0)
        active_topics = active_topics[active_topics['importance_weight'] > 0]

        if active_topics.empty:
            return []

        # Calculate probability weights based on 'importance_weight'
        # Higher weight = Higher chance of being selected
        weights = active_topics['importance_weight'].astype(float)
        
        # Select topics
        # We use random.choices which allows replacement (studying same topic multiple times is fine/good)
        try:
            selected_indices = random.choices(active_topics.index, weights=weights, k=count)
        except ValueError:
            # Fallback if weights error (though >0 check handles it)
            selected_indices = random.choices(active_topics.index, k=count)
            
        selected_topics = active_topics.loc[selected_indices]
        
        topic_list = []
        for _, row in selected_topics.iterrows():
            topic_str = f"{row['topic']} ({row['subtopic']})"
            topic_list.append({
                'lesson': row['lesson'],
                'desc': topic_str,
                'weight': row['importance_weight']
            })
            
        return topic_list

    def generate_weekly_schedule(self, start_date=None, custom_weights=None, topic_weights=None, 
                                     preserve_manual=True, start_time=None, num_blocks=5, active_days=None):
        """
        Generates a filled schedule for the upcoming week.
        
        Args:
            start_time: datetime.time object for daily start (e.g., time(15, 0))
            num_blocks: Number of study blocks per day
            active_days: List of day names (e.g., ["Monday", "Tuesday"])
            preserve_manual: If True, do not overwrite blocks manually edited by user.
        """
        from datetime import time as dt_time
        
        # Default values
        if start_time is None:
            start_time = dt_time(14, 30)
        if active_days is None:
            active_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Generate template dynamically OR use CSV fallback
        if start_time and num_blocks:
            # Dynamic Template Generation
            template_rows = []
            block_duration = 30  # minutes
            short_break = 10
            long_break = 30
            
            for day in active_days:
                current_time = datetime.combine(datetime.today(), start_time)
                block_num = 1
                
                for i in range(num_blocks):
                    # Study Block
                    block_start = current_time.strftime("%H:%M")
                    current_time += timedelta(minutes=block_duration)
                    block_end = current_time.strftime("%H:%M")
                    
                    template_rows.append({
                        "schedule_id": f"{day[:3]}_blk_{block_num}",
                        "student_id": "pilot_ogrenci_01",
                        "day_of_week": day,
                        "block_start": block_start,
                        "block_end": block_end,
                        "block_type": "etut",
                        "task_type": f"Blok {block_num}: Konu Çalışması",
                        "target_desc": "Otomatik oluşturuldu",
                        "is_active": True,
                        "is_completed": False
                    })
                    
                    # Break (alternating short/long)
                    break_duration = long_break if (block_num % 2 == 0) else short_break
                    break_start = current_time.strftime("%H:%M")
                    current_time += timedelta(minutes=break_duration)
                    break_end = current_time.strftime("%H:%M")
                    
                    if i < num_blocks - 1:  # No break after last block
                        template_rows.append({
                            "schedule_id": f"{day[:3]}_brk_{block_num}",
                            "student_id": "pilot_ogrenci_01",
                            "day_of_week": day,
                            "block_start": break_start,
                            "block_end": break_end,
                            "block_type": "uzun_mola" if break_duration == long_break else "mola",
                            "task_type": "Mola Zamanı ☕",
                            "target_desc": "Dinlen ve yenilen",
                            "is_active": True,
                            "is_completed": False
                        })
                    
                    block_num += 1
            
            template = pd.DataFrame(template_rows)
        elif os.path.exists(self.schedule_template_file):
            # Fallback to CSV
            template = pd.read_csv(self.schedule_template_file)
        else:
            return []
        
        # Identify 'etut' blocks that need filling
        indices_to_fill = []
        for idx, row in template.iterrows():
            if row['block_type'] != 'etut':
                continue
                
            if preserve_manual:
                desc = str(row.get('target_desc', ''))
                type_desc = str(row.get('task_type', ''))
                
                # Check for "Otomatik oluşturuldu" flag or generic names
                is_generic = "Blok" in desc or "Konu Çalışması" in desc or "Otomatik" in desc or "Otomatik" in type_desc
                if not is_generic and desc.strip() != "":
                    continue # Skip this block, it's manually set
            
            indices_to_fill.append(idx)

        num_etuts = len(indices_to_fill)
        
        # Get intelligent topic suggestions with weights
        topics = []
        if num_etuts > 0:
            topics = self._get_next_topics(count=num_etuts, custom_weights=custom_weights, topic_weights=topic_weights)
        
        # Fill the template
        filled_schedule = template.copy()
        filled_schedule['target_desc'] = filled_schedule['target_desc'].astype(object) # Ensure writeable
        filled_schedule['task_type'] = filled_schedule['task_type'].astype(object)

        # Calculate dates (Same as before)
        if not start_date:
            start_date = datetime.now()
            
        day_map = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
            'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }
        
        current_weekday = start_date.weekday()
        monday_date = start_date - timedelta(days=current_weekday)
        
        current_topic_idx = 0
        
        for idx in filled_schedule.index:
            row = filled_schedule.loc[idx]
            
            # Date Calc (Always Run This!)
            day_offset = day_map.get(row['day_of_week'], 0)
            actual_date = monday_date + timedelta(days=day_offset)
            filled_schedule.at[idx, 'date'] = actual_date.strftime("%Y-%m-%d")
            
            # Fill logic
            if idx in indices_to_fill and current_topic_idx < len(topics):
                topic_info = topics[current_topic_idx]
                
                # Update both description and task type for clarity
                filled_schedule.at[idx, 'target_desc'] = topic_info['desc'] # e.g. "Üslü İfadeler (Çözümleme)"
                filled_schedule.at[idx, 'task_type'] = f"📚 {topic_info['lesson']}" # e.g. "📚 Matematik"
                
                # We could add an internal flag 'is_ai_generated'
                current_topic_idx += 1
                
        return filled_schedule.to_dict('records')

    def save_active_schedule(self, schedule_data_or_df):
        """
        Saves the schedule to database.
        schedule_data_or_df: Can be list of dicts (from db) or DataFrame.
        """
        if isinstance(schedule_data_or_df, list):
            df = pd.DataFrame(schedule_data_or_df)
        elif isinstance(schedule_data_or_df, pd.DataFrame):
            df = schedule_data_or_df
        else:
            print("Unknown schedule data format.")
            return False
            
        return self.db.save_schedule(df)

    def _inject_dates(self, records: list) -> list:
        """
        Injects the calculated 'date' field into schedule records based on 'day_of_week'.
        Uses the current week's dates.
        """
        if not records:
            return []
            
        start_date = datetime.now()
        day_map = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
            'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }
        current_weekday = start_date.weekday()
        monday_date = start_date - timedelta(days=current_weekday)
        
        for row in records:
            # If date is missing, calculate it
            if 'date' not in row:
                if 'day_of_week' in row and row['day_of_week'] in day_map:
                    day_offset = day_map[row['day_of_week']]
                    actual_date = monday_date + timedelta(days=day_offset)
                    row['date'] = actual_date.strftime("%Y-%m-%d")
                else:
                    row['date'] = datetime.now().strftime("%Y-%m-%d")
                    
        return records

    def load_active_schedule(self):
        """Loads schedule from DB (or template if DB empty)."""
        # 1. Try DB
        schedule_df = self.db.load_schedule()
        if not schedule_df.empty:
            records = schedule_df.to_dict('records')
            return self._inject_dates(records)
            
        # 2. Fallback to local template if DB is empty
        if os.path.exists(self.schedule_template_file):
             template = pd.read_csv(self.schedule_template_file)
             
             # Convert template format to DB format (minimal)
             # Default values for persistence
             template['student_id'] = 'pilot_ogrenci_01'
             template['status'] = 'pending'
             template['is_active'] = True
             
             records = template.to_dict('records')
             return self._inject_dates(records)
             
        return []

def get_scheduler_engine():
    return SchedulerEngine()
