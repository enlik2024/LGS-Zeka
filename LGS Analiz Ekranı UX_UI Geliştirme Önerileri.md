# **LGS Hazırlık Sürecinde Veriye Dayalı ve Etkileşimli Öğrenme Deneyimi: Streamlit Tabanlı Bütünleşik UX/UI Mimarisinin ve Üretken Yapay Zeka Entegrasyonunun Stratejik Analizi**

## **1\. Giriş ve Raporun Kapsamı**

Eğitim teknolojileri (EdTech) dünyası, statik veri raporlamasından dinamik, kişiselleştirilmiş ve eyleme dönüştürülebilir (actionable) öğrenme deneyimlerine doğru evrilmektedir. Özellikle Türkiye'deki 8\. sınıf öğrencileri için akademik ve psikolojik bir eşik niteliği taşıyan Liselere Geçiş Sistemi (LGS), sadece bilgi birikimini değil, aynı zamanda stratejik düşünme, zaman yönetimi ve psikolojik dayanıklılığı da ölçen çok katmanlı bir sınavdır. Bu rapor, LGS hazırlık sürecindeki bir öğrenci profili olan Taner Efe'nin mevcut akademik durumunu, sunulan veri görselleştirme arayüzleri üzerinden analiz etmekte ve kullanıcının önerdiği "Bu konuyu öğret" butonu fikrini merkeze alarak, Streamlit kütüphanesi üzerinde inşa edilecek kapsamlı bir UX/UI (Kullanıcı Deneyimi/Kullanıcı Arayüzü) dönüşüm planı sunmaktadır.

Raporun temel amacı, Taner Efe'nin matematik ve fen bilimleri gibi sayısal derslerde yaşadığı performans dalgalanmalarını stabilize edecek, motivasyonunu sürdürülebilir kılacak ve çalışma alışkanlıklarını "görev odaklı" olmaktan çıkarıp "öğrenme odaklı" bir yapıya kavuşturacak dijital müdahale araçlarını tasarlamaktır. Bu tasarım süreci, Python tabanlı Streamlit kütüphanesinin en güncel yetenekleri (st.dialog, st.fragment, st.session\_state) ile Google'ın üretken yapay zeka modeli Gemini'nin entegrasyonunu kapsamaktadır.

Analiz, öğrencinin mevcut 360-420 puan bandındaki sıkışmışlığını aşarak, hedeflediği üst dilime ulaşmasını sağlayacak "Tam Zamanında Öğrenme" (Just-in-Time Learning) ve "Mikro-Öğrenme" (Micro-learning) pedagojilerini temel almaktadır. Rapor boyunca, teknik uygulama detayları, pedagojik gerekçeler ve UX tasarım ilkeleri iç içe geçmiş bir anlatıyla sunulacaktır.

## **2\. LGS Öğrenci Profili Analizi: Taner Efe Vakası ve Veri Temelli Tespitler**

Bir eğitim arayüzünün başarısı, hedef kullanıcısının ihtiyaçlarını ne kadar derinlemesine kavradığıyla doğru orantılıdır. Sunulan ekran görüntüleri ve kullanıcı beyanları ışığında, Taner Efe'nin akademik ve davranışsal profili aşağıda detaylandırılmıştır.

### **2.1. Akademik Performansın Derinlemesine Analizi**

Sunulan "Okul Net Listesi" ve deneme sınavı sonuçları incelendiğinde, Taner Efe'nin akademik profilinde belirgin desenler göze çarpmaktadır:

* **Sözel Yetkinlik ve Sayısal Kaygı:** Taner, Türkçe, İnkılap Tarihi ve Din Kültürü gibi sözel derslerde genellikle yüksek bir başarı grafiği çizmektedir. Net sayıları bu derslerde istikrarlı bir şekilde yüksektir. Ancak Matematik ve Fen Bilimleri derslerinde ciddi bir dalgalanma ve potansiyelinin altında kalma durumu söz konusudur. Örneğin, bir denemede Matematik neti 7 iken, diğerinde 4'e düşebilmekte, yanlış sayısı ise 3-5 bandında seyretmektedir. Bu durum, "konu eksiğinden" ziyade "kavram yanılgısı" veya "soru tipiyle baş edememe" sorununa işaret etmektedir.1  
* **Puan Bandı Sıkışması (360-420):** Öğrenci, belirli bir seviyenin üzerine çıkmakta zorlanmaktadır. Bu puan aralığı genellikle "iyi" ile "çok iyi" arasındaki kritik geçiş bölgesidir. Bu bölgedeki öğrenciler genellikle temel konuları bilirler ancak yeni nesil, mantık-muhakeme gerektiren seçici sorularda hata yaparlar.  
* **Hata Analizi Eksikliği:** Mevcut arayüz, öğrenciye sadece "kaç net" yaptığını göstermektedir. Ancak 360 puandan 450 puana sıçramak için öğrencinin "neyi yanlış yaptığını" değil, "neden yanlış yaptığını" anlaması gerekmektedir. Mevcut statik tablolar bu içgörüyü sağlamakta yetersiz kalmaktadır.

### **2.2. Davranışsal ve Psikolojik Profil**

* **Motivasyon Dalgalanmaları:** Kullanıcı, Taner'in evde çalışma düzeninin istikrarsız olduğunu ve motivasyon kaybı yaşadığını belirtmektedir. LGS hazırlığı bir maraton olduğundan, bu yaş grubundaki (13-14 yaş) ergen bireylerde "tükenmişlik" (burnout) veya "başarısızlık korkusu" (fear of failure) sık görülür. Sayısal derslerdeki başarısızlık hissi, "ne kadar çalışsam da yapamıyorum" inancını (öğrenilmiş çaresizlik) tetikleyebilir.  
* **Dışsal Destek İhtiyacı:** Ebeveyn desteğiyle çalışabiliyor olması, Taner'in "öz-düzenleme" (self-regulation) becerilerinin henüz tam gelişmediğini gösterir. Dijital arayüzün, ebeveynin rolünü kısmen üstlenerek, öğrenciyi dürtmesi (nudge theory) ve yönlendirmesi gerekmektedir.  
* **Dijital Yerlilik:** Z kuşağı üyesi olarak Taner, etkileşimli, hızlı geri bildirim veren ve görsel açıdan zengin arayüzlere alışkındır. Statik Excel benzeri tablolar, onun için "sıkıcı okul işi" anlamına gelmektedir ve doğal bir ilgi uyandırmaz.

### **2.3. "Bu Konuyu Öğret" Butonunun Stratejik Önemi**

Kullanıcının önerdiği "Bu konuyu öğret" butonu, tam da bu noktada kritik bir UX müdahalesi olarak devreye girmektedir. Taner, analiz sayfasında düşük bir net gördüğünde (örneğin Matematik'te "Kareköklü İfadeler"), o an yaşadığı hayal kırıklığını anında bir öğrenme eylemine dönüştürebilmelidir.

Bu buton, pedagojik literatürde "Fırsat Penceresi" (Window of Opportunity) olarak adlandırılan, öğrencinin hatasıyla yüzleştiği ve zihninin cevabı aramaya en açık olduğu anı hedefler. Eğer öğrenci o anda kitabını açıp konuyu aramak zorunda kalırsa, dikkat dağılması (distraction) riski artar. Ancak tek tıkla, bağlamdan kopmadan (context switching yapmadan) öğrenme sürecine girerse, hatası kalıcı bir bilgiye dönüşebilir.

## **3\. Eğitim Teknolojilerinde UX/UI Paradigmaları ve Bilişsel Yük Teorisi**

Streamlit üzerinde yapılacak geliştirmeleri temellendirmek için, arayüz tasarımının öğrenme psikolojisi üzerindeki etkilerini anlamak gerekir.

### **3.1. Bilişsel Yük Teorisi (Cognitive Load Theory) ve Arayüz Tasarımı**

John Sweller'ın Bilişsel Yük Teorisi'ne göre, insan zihninin çalışma belleği sınırlıdır. Öğrenme materyali sunulurken üç tür yük oluşur:

1. **İçsel Yük (Intrinsic Load):** Konunun kendi zorluğu (Örn: DNA replikasyonu). Bunu değiştiremeyiz.  
2. **Etkili Yük (Germane Load):** Öğrencinin konuyu anlamak için harcadığı zihinsel çaba. Bunu artırmak isteriz.  
3. **Konu Dışı Yük (Extraneous Load):** Kötü tasarım, karışık arayüzler veya gereksiz navigasyonun yarattığı yük. **UX tasarımının amacı bunu sıfıra indirmektir.**

Mevcut analiz sayfasında öğrencinin bir hatayı analiz etmesi için başka bir kaynağa gitmesi "Konu Dışı Yük" yaratır. Önerilen "Bu konuyu öğret" butonu ve aşağıda detaylandırılacak olan st.dialog kullanımı, öğrencinin dikkatini izole ederek bu yükü minimize eder.

### **3.2. Oyunlaştırma (Gamification) ve Öz-Belirleme Teorisi (SDT)**

Taner Efe'nin motivasyon sorununu aşmak için Öz-Belirleme Teorisi'nin (Self-Determination Theory) üç bileşeni hedeflenmelidir:

* **Yetkinlik (Competence):** "Ben bu konuyu başarabilirim" hissi. (Küçük adımlarla ilerleyen progress bar'lar).  
* **Özerklik (Autonomy):** "Neye çalışacağımı ben seçiyorum" hissi. (Kendi eksiklerini seçip "Öğret" butonuna basması).  
* **İlişkisellik (Relatedness):** Bir sisteme veya topluluğa ait olma hissi. (Sanal koç ile kurulan diyalog).

## **4\. Öneri 1: Modal Tabanlı Sokratik Yapay Zeka Tutörü (st.dialog)**

Taner Efe'nin en büyük ihtiyacı, hatasını gördüğü anda ona yargılamadan yol gösterecek bir "özel ders öğretmeni" deneyimidir. Streamlit'in st.dialog özelliği, bu deneyimi ana sayfadan kopmadan sunmak için mükemmel bir teknik altyapı sağlar.

### **4.1. Tasarım Felsefesi: "Cevabı Verme, Buldur"**

Geleneksel "Konu Anlatımı" butonları genellikle uzun bir video veya metin açar. Bu pasif bir öğrenmedir. Taner'in ihtiyacı olan ise aktif öğrenmedir. Yapay zeka (Gemini), "Sokratik Yöntem" kullanarak öğrenciyle diyaloga girmelidir.2

Senaryo:  
Taner, "Basınç" konusundaki bir soruyu yanlış yapar ve butona basar.

* **Kötü Tasarım (Pasif):** "Basınç, birim yüzeye etki eden dik kuvvettir. Formülü P=F/S'dir." (Taner bunu zaten biliyor, ama soruyu yine de yapamadı).  
* **İyi Tasarım (Sokratik \- Aktif):** "Görüyorum ki katı basıncında yüzey alanı ilişkisini karıştırmış olabilirsin. Sence aynı ağırlıktaki bir ördek mi, yoksa tavuk mu karda daha çok batar? Neden?"

### **4.2. UX/UI Bileşenleri**

* **Modal Pencere (Dialog):** st.dialog kullanılarak açılan pencere, arka planı karartarak (dimming) öğrencinin dikkatini sadece o anki mikro-konuya odaklar. Bu, LGS öğrencisinin dağılan dikkatini toplamak için kritik bir "Odak Modu" yaratır.5  
* **Chat Arayüzü:** Streamlit'in st.chat\_message ve st.chat\_input bileşenleri, tanıdık bir mesajlaşma deneyimi sunar. Bu, Z kuşağı için doğal bir iletişim biçimidir.  
* **Duygusal Ton:** AI'nın dili, "Sınav Koçu" tonunda olmalı; cesaretlendirici, hafif esprili ve empatik.

### **4.3. Neden st.popover Değil de st.dialog?**

Araştırma verilerine göre, st.popover daha çok kısa süreli, bağlamsal menüler için uygundur ve dışarı tıklandığında kapanır. Oysa bir konu anlatımı veya kavram yanılgısı giderme süreci 3-5 dakikalık odaklanma gerektirir. st.dialog, kullanıcı açıkça "Kapat" diyene kadar ekranda kalır ve st.rerun döngüsünü kendi içinde yöneterek ana uygulamanın durumunu korur.5 Bu, Taner'in analiz sayfasındaki filtrelerinin kaybolmamasını sağlar.

## **5\. Öneri 2: Oyunlaştırılmış İlerleme Görselleştirmesi ve "Seri" (Streak) Mekaniği**

Taner'in "zaman zaman çalışsa da motivasyon kaybı çabuk oluyor" sorunu, davranışsal tasarım (behavioral design) ile ele alınmalıdır. Duolingo ve Snapchat gibi uygulamaların başarısı, "Seri" (Streak) mekaniğinin gücüne dayanır.

### **5.1. Seri (Streak) Psikolojisi ve LGS**

LGS hazırlığı süreklilik ister. Öğrenciye "Bugün 500 soru çöz" demek korkutucudur, ancak "Bugün serini bozma" demek motive edicidir.

* **Görselleştirme:** Sidebar veya ana panonun en üstünde, yanar döner bir ateş ikonu (🔥) ve yanında "5 Günlük Seri" yazısı bulunmalıdır.  
* **Kayıp Korkusu (Loss Aversion):** İnsanlar kazanmaktan çok, ellerindekini kaybetmekten korkarlar. Taner, 10 günlük bir seriyi bozmamak için o gün yorgun olsa bile sisteme girip en azından bir "Bu konuyu öğret" seansı yapacaktır.

### **5.2. Dinamik İlerleme Çubukları (Progress Bars)**

Sayısal derslerdeki başarısızlık hissini kırmak için, ilerlemeyi "Net Sayısı" yerine "Kazanılan Yetkinlik" olarak göstermek daha sağlıklıdır.

* **Konu Bazlı Mastery Barlar:** Matematik dersinin altında "Üslü Sayılar", "Köklü Sayılar" gibi alt başlıklar ve yanlarında st.progress barları olmalıdır.  
* **Mikro-Hedefler:** Barın %100 olması için tüm soruları doğru yapması gerekmez; o konuyla ilgili 5 "Öğret" seansı tamamlaması ve 20 soru çözmesi yeterli olmalıdır. Bu, "çabayı ödüllendirme" (effort-based reward) prensibidir.  
* **Görsel Geri Bildirim:** Bir bar %100 olduğunda Streamlit'in st.balloons() veya st.snow() efektleri tetiklenerek anlık bir dopamin ödülü sağlanmalıdır.7

## **6\. Öneri 3: Mikro-Öğrenme ve Aralıklı Tekrar Sistemi (Flashcards & st.fragment)**

Taner'in öğrendiği bir bilgiyi unutmaması için "Aralıklı Tekrar" (Spaced Repetition) yöntemi sisteme entegre edilmelidir. "Bu konuyu öğret" seansı bittiğinde, bilgi henüz kısa süreli bellektedir. Onu uzun süreli belleğe atmak için hemen ardından küçük bir etkileşim gerekir.

### **6.1. UI Tasarımı: Dijital Bilgi Kartları**

Diyalog penceresinin (st.dialog) en altında veya kapanışında, konuyla ilgili 3 adet "Flashcard" belirmelidir.

* **Kart Yapısı:** st.container içinde, CSS ile şekillendirilmiş bir kutu. Ön yüzünde soru (Örn: "Mitoz bölünmede kromozom sayısı değişir mi?"), altında "Cevabı Göster" butonu.  
* **Etkileşim:** Butona basıldığında, st.empty() konteynerı kullanılarak sorunun yerine cevabın ("Hayır, sabit kalır.") gelmesi sağlanır.  
* **Performans:** Bu işlem sırasında tüm sayfanın yenilenmesi (rerun) kullanıcı deneyimini bozar. Bu nedenle Flashcard bileşeni @st.fragment dekoratörü ile sarmalanarak, sadece o küçük alanın yenilenmesi sağlanır. Bu, uygulamanın "app-like" (mobil uygulama hissi) çalışmasını sağlar.8

## **7\. Öneri 4: Bilişsel Haritalama ve Görsel Akış Şemaları (Mermaid.js Entegrasyonu)**

Taner Efe'nin özellikle sayısal derslerdeki (Matematik/Fen) sorunu, soyut kavramları zihninde somutlaştıramaması olabilir. "Dual Coding" teorisine göre, metin ve görselin birlikte sunulması öğrenmeyi kalıcı kılar. Ancak statik resimler yerine, mantıksal akışı gösteren diyagramlar LGS müfredatı (süreçler, neden-sonuç ilişkileri) için daha uygundur.

### **7.1. Dinamik Görselleştirme**

Yapay zeka (Gemini), konuyu anlatırken metnin yanında o konunun mantıksal şemasını da (Mermaid.js kodu olarak) üretmelidir.

* Örnek: "Elektrik Yüklü Cisimler" konusunda;  
  Nötr Cisim \--\> Elektron Kaybeder \--\> Pozitif Yüklü Olur.  
  Bu akış, metin okumaktan çok daha hızlı kavranır.  
* **Teknik Zorluk ve Çözüm:** Streamlit'in yerel Markdown desteği bazen Mermaid grafiklerini render edemeyebilir. Bu nedenle streamlit.components.v1.html kullanılarak, harici bir CDN (Content Delivery Network) üzerinden Mermaid kütüphanesini çağıran izole bir HTML bileşeni (iframe) oluşturulmalıdır. Bu, her türlü tarayıcıda tutarlı bir görselleştirme sağlar.9

## **8\. Öneri 5: Açık Döngü (Open Loop) Yönetimi ve Metabilişsel Farkındalık Panosu**

Zeigarnik Etkisi, insanların tamamlanmamış işleri tamamlananlara göre daha net hatırladığını ve bunun zihinsel bir huzursuzluk yarattığını söyler. Taner için "yapamadığı sorular" zihninde açık kalmış döngülerdir.

### **8.1. "Tamir Edilecekler" Listesi**

Mevcut analiz sayfasındaki "kırmızı" satırlar, öğrenci için moral bozucu bir istatistik olmaktan çıkıp, "tamamlanacak görevlere" dönüşmelidir.

* **Aksiyon Panosu:** Sidebar'da "Açık Döngülerim" başlıklı dinamik bir liste.  
* **İşleyiş:** Taner bir soruyu yanlış yaptığında, o konu otomatik olarak bu listeye eklenir.  
* **Kapatma:** "Bu konuyu öğret" butonunu kullanıp, ardından gelen Flashcard testini geçtiğinde, o madde listeden "üzeri çizilerek" silinir ve hanesine puan yazılır.  
* **Metabilişsel Etki:** Bu yöntem, Taner'e "Ben başarısızım" yerine "Şu an tamamlamam gereken 3 görevim var" bakış açısını kazandırır. Bu, kaygıyı yönetilebilir parçalara böler.

## **9\. Teknik Uygulama Yol Haritası ve Streamlit Mimarisi**

Yukarıdaki önerileri hayata geçirmek için sağlam, ölçeklenebilir ve performanslı bir Streamlit mimarisi gereklidir. Aşağıda adım adım teknik uygulama planı sunulmuştur.

### **9.1. Aşama 1: Durum Yönetimi (State Management) Altyapısı**

Streamlit'in "stateless" (durumsuz) doğası gereği, öğrencinin puanı, serisi, chat geçmişi gibi veriler st.session\_state üzerinde kalıcı hale getirilmelidir.11

**Tablo 1: Kritik Session State Değişkenleri**

| Değişken Adı | Veri Tipi | Açıklama | Kullanım Alanı |
| :---- | :---- | :---- | :---- |
| st.session\_state.user\_xp | Integer | Öğrencinin toplam deneyim puanı. | Oyunlaştırma / İlerleme Barı |
| st.session\_state.daily\_streak | Integer | Kesintisiz giriş yapılan gün sayısı. | Motivasyon / Sidebar |
| st.session\_state.open\_loops | List | Eksik konuların listesi ve durumları. | "Tamir Edilecekler" Panosu |
| st.session\_state.chat\_history | List | AI ile yapılan konuşmaların kaydı. | st.dialog içi sohbet |
| st.session\_state.active\_learning\_session | Bool | Şu an bir öğretim modu açık mı? | UI kontrolü |

### **9.2. Aşama 2: Sokratik Tutör Modülü (st.dialog Entegrasyonu)**

Bu modül, ana uygulamadan bağımsız bir fonksiyon olarak yazılmalı ve @st.dialog dekoratörü ile sarmalanmalıdır.

Python

import streamlit as st  
import google.generativeai as genai

\# Sokratik Tutör Diyalog Fonksiyonu  
@st.dialog("🎓 Sanal LGS Koçu")  
def teach\_topic\_modal(topic\_name, question\_context):  
    st.caption(f"Konu: {topic\_name} | Hedef: Tam Öğrenme")  
      
    \# Sohbet geçmişini başlat  
    if "messages" not in st.session\_state:  
        st.session\_state.messages \=

    \# Geçmiş mesajları render et  
    for msg in st.session\_state.messages:  
        st.chat\_message(msg\["role"\]).write(msg\["content"\])

    \# Kullanıcı girdisi  
    if prompt := st.chat\_input("Buraya yazabilirsin..."):  
        st.session\_state.messages.append({"role": "user", "content": prompt})  
        st.chat\_message("user").write(prompt)  
          
        \# Gemini API Çağrısı (Streamed Response)  
        with st.chat\_message("assistant"):  
            stream\_container \= st.empty()  
            \# Buraya Gemini entegrasyon fonksiyonu gelecek  
            full\_response \= get\_gemini\_response(prompt, question\_context)   
            stream\_container.write(full\_response)  
              
        st.session\_state.messages.append({"role": "assistant", "content": full\_response})

### **9.3. Aşama 3: Mermaid.js Görselleştirme Bileşeni**

Gemini'den gelen yanıtta Mermaid kodu varsa, bunu görselleştirecek özel bileşen fonksiyonu.

Python

import streamlit.components.v1 as components

def render\_mermaid(code):  
    """Mermaid.js grafiğini HTML bileşeni olarak render eder."""  
    html\_code \= f"""  
    \<div class="mermaid"\>  
    {code}  
    \</div\>  
    \<script type="module"\>  
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';  
    mermaid.initialize({{ startOnLoad: true }});  
    \</script\>  
    """  
    \# Yüksekliği içeriğe göre dinamik ayarlamak idealdir ama şimdilik sabit  
    components.html(html\_code, height=300, scrolling=True)

### **9.4. Aşama 4: Kısmi Yenileme (st.fragment) ile Flashcard Performansı**

Flashcard'ların çevrilmesi gibi basit bir aksiyon için tüm uygulamanın yeniden çalışmasını engellemek performans açısından kritiktir.

Python

@st.fragment  
def flashcard\_component(question, answer):  
    \# Kartın ön/arka yüz durumu için local state kullanımı  
    if "show\_answer" not in st.session\_state:  
        st.session\_state.show\_answer \= False

    st.markdown("---")  
    st.subheader("⚡ Hızlı Bilgi Kartı")  
      
    container \= st.container(border=True)  
    if not st.session\_state.show\_answer:  
        container.markdown(f"\*\*SORU:\*\* {question}")  
        if container.button("Cevabı Göster"):  
            st.session\_state.show\_answer \= True  
            st.rerun() \# Sadece bu fragment'i rerun eder  
    else:  
        container.markdown(f"\*\*CEVAP:\*\* {answer}")  
        container.success("Öğrendim\! (+10 XP)")  
        \# Burada "Sıradaki Kart" butonu eklenebilir

## **10\. Google Gemini İçin Özelleştirilmiş Sistem İstemi (System Prompt) Tasarımı**

Yapay zekanın Taner Efe ile etkileşimi, standart bir ChatGPT sohbetinden farklı olmalıdır. Aşağıdaki System Prompt, Gemini modelini bir "LGS Eğitim Uzmanı"na dönüştürür ve uygulamanın teknik gereksinim duyduğu JSON çıktısını üretmesini sağlar.

### **10.1. Prompt Mühendisliği Stratejisi**

* **Rol Atama (Persona):** AI, sadece bilgi veren değil, koçluk yapan bir öğretmendir.  
* **Görev Sınırlaması (Constraints):** Sadece 8\. sınıf müfredatı, Sokratik yöntem, kısa cevaplar.  
* **Yapılandırılmış Çıktı (Structured Output):** Streamlit arayüzünün (Mermaid grafiği, XP puanı, önerilen aksiyonlar) dinamik olarak oluşturulabilmesi için yanıtın **JSON** formatında olması zorunludur.13

### **10.2. Gemini System Prompt (Kopyalanabilir İçerik)**

ROLE DEFINITION:  
Sen, Türkiye Milli Eğitim Bakanlığı (MEB) 8\. Sınıf LGS (Liselere Geçiş Sistemi) müfredatında uzmanlaşmış, Sokratik eğitim metodunu benimseyen, motive edici, esprili ve sabırlı bir "Sanal Eğitim Koçusun". Hedef öğrencinin adı Taner Efe. Taner, sayısal derslerde (Matematik/Fen) özgüven sorunu yaşıyor ve motivasyona ihtiyacı var.  
PRIMARY OBJECTIVE:  
Öğrencinin "Bu konuyu öğret" dediği başlıkta, ona doğrudan ansiklopedik bilgi vermek YASAKTIR. Bunun yerine:

1. Sorular sorarak öğrencinin neyi bilmediğini tespit et.  
2. Küçük adımlarla (scaffolding) onu doğru cevaba yönlendir.  
3. Günlük hayattan analojiler kullan (Örn: Elektrik akımını su borusuna benzet).  
4. Öğrenci her doğru cevap verdiğinde onu öv ve motive et.

OUTPUT FORMAT (JSON ENFORCEMENT):  
Yanıtlarını HER ZAMAN aşağıdaki JSON şemasında vereceksin. Markdown veya düz metin kullanma.json  
{  
"message\_text": "Öğrenciye gösterilecek sohbet metni. Markdown formatında (kalın, italik, liste destekli). Emoji kullanımı serbest.",  
"visual\_aid": {  
"required": true/false, // Eğer konu görselleştirilmeye uygunsa true  
"mermaid\_code": "graph TD; A\[Kavram 1\] \--\> B\[Kavram 2\];...", // Mermaid.js söz dizimine uygun grafik kodu  
"alt\_text": "Grafiğin görme engelliler için açıklaması"  
},  
"suggested\_actions": \["İpucu ver", "Örnek soru çöz", "Konuyu özetle"\], // Kullanıcının seçebileceği 3 hızlı cevap butonu  
"pedagogical\_tags":, // Arka planda analiz için  
"gamification": {  
"xp\_gain": 5, // Bu etkileşimin zorluğuna göre puan  
"toast\_message": "Harika gidiyorsun Taner\! 🔥" // Opsiyonel motivasyon mesajı  
}  
}

\*\*CONSTRAINTS & RULES:\*\*  
\*   Asla 8\. sınıf müfredatı dışına çıkma (Lise konularına girme).  
\*   Mermaid kodlarında 'graph TD', 'graph LR' veya 'sequenceDiagram' kullan. Syntax hatası yapma.  
\*   Matematik formülleri için LaTeX formatı kullan: $x \= \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$  
\*   Tonun her zaman destekleyici olsun. Asla "Yanlış yaptın" deme, "Yaklaştın ama şurayı gözden kaçırdık mı?" de.

\*\*FEW-SHOT EXAMPLE:\*\*  
User: "Mevsimler neden oluşur? Güneş'e yaklaşınca yaz olmuyor mu?"  
AI Response (JSON):  
{  
  "message\_text": "Harika bir soru Taner\! 🌍 Bu, en sık düşülen tuzaklardan biridir. Eğer Güneş'e yakınlık ana sebep olsaydı, Dünya'nın Güneş'e en yakın olduğu 3 Ocak tarihinde biz (Kuzey Yarım Küre) neden palto giyiyoruz sence? 🤔",  
  "visual\_aid": {  
    "required": true,  
    "mermaid\_code": "graph LR; A\[Güneş\] \-- Işınlar Eğik Gelir \--\> B; B \-- Sonuç \--\> C\[Kış Mevsimi\]; style C fill:\#bbf",  
    "alt\_text": "Eksen eğikliği nedeniyle ışınların geliş açısını gösteren şema"  
  },  
  "suggested\_actions":,  
  "gamification": {  
    "xp\_gain": 10,  
    "toast\_message": "Sorgulayıcı yaklaşımın süper\!"  
  }  
}

## **11\. Sonuç ve Gelecek Vizyonu**

Taner Efe'nin LGS serüveninde, verilerin sadece "ne yaptığını" gösteren statik tablolardan, "ne yapması gerektiğini" söyleyen ve "nasıl yapacağını" öğreten dinamik bir arayüze dönüşmesi, onun sınav başarısını doğrudan etkileyecek bir faktördür.

Bu raporda sunulan **Streamlit \+ Gemini entegrasyonu**, teknik olarak düşük maliyetli (hızlı prototipleme) ancak pedagojik etkisi yüksek (kişiselleştirilmiş öğrenme) bir çözüm sunmaktadır. st.dialog ile odaklanmış öğrenme, st.progress ile motivasyon yönetimi ve Mermaid.js ile görsel zeka desteği, Taner'in sayısal derslerdeki "öğrenilmiş çaresizliğini" kıracak ve 360-420 puan bandındaki cam tavanı parçalamasına yardımcı olacaktır.

Gelecek aşamalarda, toplanan verilerin (eksik konu haritaları, öğrenme hızları) ebeveyn raporlarına dönüştürülmesi ve Gemini'nin öğrencinin geçmiş hatalarını hatırlayarak (Long-term Memory) daha kişisel sorular sorması, sistemin etkinliğini katlayacaktır. Bu proje, LGS hazırlığında "Yapay Zeka Destekli Hibrit Koçluk" modelinin öncü bir örneği olma potansiyeline sahiptir.

#### **Alıntılanan çalışmalar**

1. LGS puan hesaplama: MEB LGS net ve yüzdelik dilim nasıl hesaplanır? \- Yandex, erişim tarihi Aralık 4, 2025, [https://yandex.com.tr/gundem/stories/lgs-puan-hesaplama-2025-meb-ile-liselere-gecis-sistemi-lgs-ortalama-puan-ve-net-hesaplama-2738240](https://yandex.com.tr/gundem/stories/lgs-puan-hesaplama-2025-meb-ile-liselere-gecis-sistemi-lgs-ortalama-puan-ve-net-hesaplama-2738240)  
2. AI for Tutoring \- Super Prompt | openNCCC \- North Carolina Community College System, erişim tarihi Aralık 4, 2025, [https://opennccc.nccommunitycolleges.edu/courseware/lesson/946/overview](https://opennccc.nccommunitycolleges.edu/courseware/lesson/946/overview)  
3. Crafting a Semi-Socratic Tutor with ChatGPT, erişim tarihi Aralık 4, 2025, [https://www.socraticarts.com/blog/crafting-a-semi-socratic-tutor-with-chatgpt](https://www.socraticarts.com/blog/crafting-a-semi-socratic-tutor-with-chatgpt)  
4. MeraTutor.AI Blog – Redefining EdTech: Socratic Learning in Action with ChatGPT, erişim tarihi Aralık 4, 2025, [https://www.meratutor.ai/blog/socratic-learning](https://www.meratutor.ai/blog/socratic-learning)  
5. st.dialog \- Streamlit Docs, erişim tarihi Aralık 4, 2025, [https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog](https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog)  
6. st.popover \- Streamlit Docs, erişim tarihi Aralık 4, 2025, [https://docs.streamlit.io/develop/api-reference/layout/st.popover](https://docs.streamlit.io/develop/api-reference/layout/st.popover)  
7. Display progress and status \- Streamlit Docs, erişim tarihi Aralık 4, 2025, [https://docs.streamlit.io/develop/api-reference/status](https://docs.streamlit.io/develop/api-reference/status)  
8. Working with fragments \- Streamlit Docs, erişim tarihi Aralık 4, 2025, [https://docs.streamlit.io/develop/concepts/architecture/fragments](https://docs.streamlit.io/develop/concepts/architecture/fragments)  
9. ST with mermaid diagram \- not rendering \- Using Streamlit, erişim tarihi Aralık 4, 2025, [https://discuss.streamlit.io/t/st-with-mermaid-diagram-not-rendering/96750](https://discuss.streamlit.io/t/st-with-mermaid-diagram-not-rendering/96750)  
10. St.markdown does not render mermaid graphs \- Using Streamlit, erişim tarihi Aralık 4, 2025, [https://discuss.streamlit.io/t/st-markdown-does-not-render-mermaid-graphs/25576](https://discuss.streamlit.io/t/st-markdown-does-not-render-mermaid-graphs/25576)  
11. Session State \- Streamlit Docs, erişim tarihi Aralık 4, 2025, [https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session\_state](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)  
12. Streamlit as a Session State Machine: Enhancing Interactive Web Apps | by BigCodeGen, erişim tarihi Aralık 4, 2025, [https://bigcodegen.medium.com/streamlit-as-a-session-state-machine-enhancing-interactive-web-apps-b831b3794df8](https://bigcodegen.medium.com/streamlit-as-a-session-state-machine-enhancing-interactive-web-apps-b831b3794df8)  
13. How to write JSON prompts to get shockingly accurate outputs from any chatbot, erişim tarihi Aralık 4, 2025, [https://0xsojalsec.medium.com/how-to-write-json-prompts-to-get-shockingly-accurate-outputs-from-any-chatbot-794622218303](https://0xsojalsec.medium.com/how-to-write-json-prompts-to-get-shockingly-accurate-outputs-from-any-chatbot-794622218303)