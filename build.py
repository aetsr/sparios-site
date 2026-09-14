#!/usr/bin/env python3
"""Builds the static Sparios legal & support site (TR/EN/DE) into docs/ for GitHub Pages.

Only public web copy lives in this repository — no app source code.
Run: python3 build.py
"""
import html
import os
import shutil

OUT = "docs"
EMAIL = "tasarahmeteren@gmail.com"
UPDATED = {"tr": "14 Eylül 2026", "en": "14 September 2026", "de": "14. September 2026"}
LANGS = ["tr", "en", "de"]
PAGES = ["privacy", "terms", "support", "accessibility"]
EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"

UI = {
    "tr": {
        "home": "Ana sayfa", "privacy": "Gizlilik", "terms": "Kullanım Koşulları", "support": "Destek",
        "accessibility": "Erişilebilirlik", "updated": "Son güncelleme", "contact": "İletişim",
        "tagline": "Harcamalarını cihazında tutan, sakin bir harcama defteri.",
        "intro": "Sparios, Apple Pay ödemelerini ve elle girdiğin harcamaları yalnızca iPhone’unda saklar, kategorilere ayırır ve ay sonunu önceden görmene yardım eder. Hesap yok, sunucu yok, reklam yok.",
        "footer": "Sparios bağımsız bir geliştirici tarafından yapılmıştır. Apple, Apple Pay ve iPhone, Apple Inc.’in ticari markalarıdır.",
        "lang": "Dil",
    },
    "en": {
        "home": "Home", "privacy": "Privacy", "terms": "Terms of Use", "support": "Support",
        "accessibility": "Accessibility", "updated": "Last updated", "contact": "Contact",
        "tagline": "A calm spending journal that keeps your data on your device.",
        "intro": "Sparios keeps your Apple Pay payments and the expenses you add by hand on your iPhone only, sorts them into categories and helps you see the end of the month coming. No account, no server, no ads.",
        "footer": "Sparios is made by an independent developer. Apple, Apple Pay and iPhone are trademarks of Apple Inc.",
        "lang": "Language",
    },
    "de": {
        "home": "Start", "privacy": "Datenschutz", "terms": "Nutzungsbedingungen", "support": "Support",
        "accessibility": "Barrierefreiheit", "updated": "Zuletzt aktualisiert", "contact": "Kontakt",
        "tagline": "Ein ruhiges Ausgabenbuch, das deine Daten auf deinem Gerät lässt.",
        "intro": "Sparios speichert deine Apple-Pay-Zahlungen und manuell erfassten Ausgaben ausschließlich auf deinem iPhone, ordnet sie Kategorien zu und hilft dir, das Monatsende kommen zu sehen. Kein Konto, kein Server, keine Werbung.",
        "footer": "Sparios wird von einem unabhängigen Entwickler erstellt. Apple, Apple Pay und iPhone sind Marken der Apple Inc.",
        "lang": "Sprache",
    },
}

SUMMARY = {
    "privacy": {
        "tr": "Sparios hiçbir kişisel veri toplamaz. Her şey iPhone’unda kalır.",
        "en": "Sparios collects no personal data. Everything stays on your iPhone.",
        "de": "Sparios erhebt keine personenbezogenen Daten. Alles bleibt auf deinem iPhone.",
    },
    "terms": {
        "tr": "Uygulamayı ve Sparios Pro aboneliğini hangi koşullarla kullandığın.",
        "en": "The terms for using the app and the Sparios Pro subscription.",
        "de": "Die Bedingungen für die App und das Sparios-Pro-Abo.",
    },
    "support": {
        "tr": "Otomasyon kurulumu, abonelik, cihaz değiştirme ve sık sorulanlar.",
        "en": "Automation setup, subscription, switching iPhones and common questions.",
        "de": "Automations-Einrichtung, Abo, iPhone-Wechsel und häufige Fragen.",
    },
    "accessibility": {
        "tr": "Sparios’u herkesin rahatça kullanabilmesi için neler yaptık.",
        "en": "What we do so everyone can use Sparios comfortably.",
        "de": "Was wir tun, damit alle Sparios bequem nutzen können.",
    },
}

# Page bodies: list of (heading, [paragraph html, ...]). Inline <strong>/<a> allowed.
CONTENT = {
"privacy": {
"tr": [
("Kısaca", [
"Sparios bir hesap istemez, bir sunucuya bağlanmaz ve senin hakkında hiçbir veri toplamaz, satmaz ya da paylaşmaz. Harcamaların, kategorilerin, hedeflerin ve Asistan sohbetlerin yalnızca iPhone’undaki uygulama klasöründe saklanır.",
"Uygulamada reklam, analiz, izleme veya çökme raporlama aracı yoktur. App Store gizlilik etiketimiz bu yüzden “Veri Toplanmaz”dır.",
]),
("Cihazında saklananlar", [
"Harcama kayıtları (tutar, para birimi, işletme adı, tarih, isteğe bağlı kart etiketi ve not), kategoriler ve öğrenilen kategori kuralları, harcama hedefleri, içgörülere verdiğin geri bildirimler, Asistan sohbet geçmişi ve uygulama tercihlerin.",
"Otomasyonun neden kayıt oluşturmadığını anlamana yardım eden yerel bir tanılama günlüğü tutulur. Bu günlük tutar, işletme adı veya kart bilgisi içermez; yalnızca alanların gelip gelmediğini kaydeder, en fazla 7 gün saklanır ve Ayarlar’dan kapatılıp temizlenebilir.",
"Veriler iOS dosya veri korumasıyla saklanır ve uygulama yedeğinden (iCloud/bilgisayar yedeği) hariç tutulur. Bu, uygulamayı silersen verilerin de silineceği anlamına gelir.",
]),
("Apple Pay otomasyonu", [
"Sparios, Cüzdan geçmişini veya banka hesabını okumaz. Kayıtlar yalnızca senin Kestirmeler uygulamasında kendin kurduğun otomasyon Sparios’a bir ödeme gönderdiğinde oluşur. Hangi kartların izleneceğine sen karar verirsin.",
]),
("Asistan", [
"Asistan, Apple’ın cihaz içi dil modelini (Apple Intelligence) kullanır. Soruların ve yanıtlar iPhone’undan çıkmaz; hiçbir bulut yapay zekâ hizmetine gönderilmez. Model harcamalarını değiştiremez veya silemez.",
]),
("Bildirimler", [
"Tüm bildirimler cihazında oluşturulur. Kilit ekranında işletme adı veya tutar gösterilmez.",
]),
("Başka bir iPhone’a aktarma", [
"Verilerini yeni iPhone’una taşımak istediğinde iki cihaz yerel ağ veya Bluetooth üzerinden, uçtan uca şifreli ve doğrudan birbirine bağlanır. Veriler hiçbir sunucudan geçmez. Bağlantıyı yalnızca yeni iPhone’da gösterilen 6 haneli kodu girerek başlatabilirsin.",
]),
("Satın almalar", [
"Sparios Pro aboneliği tamamen Apple tarafından işlenir. Ödeme bilgilerin bize ulaşmaz; uygulama yalnızca Apple’dan aboneliğinin etkin olup olmadığını öğrenir.",
]),
("Verilerini silmek", [
"Ayarlar › Veri yönetimi › <strong>Tüm verilerimi sil</strong> harcamaları, kuralları, hedefleri, sohbetleri ve planlanmış bildirimleri kalıcı olarak siler. Uygulamayı silmek de tüm verileri kaldırır.",
]),
("Çocuklar", [
"Sparios çocuklardan bilerek veri toplamaz; zaten kimseden veri toplamaz.",
]),
("Değişiklikler ve iletişim", [
"Bu politikayı değiştirirsek güncel tarih bu sayfada yer alır. Soruların için: <a href=\"mailto:{email}\">{email}</a>",
]),
],
"en": [
("In short", [
"Sparios doesn’t ask for an account, doesn’t connect to a server, and doesn’t collect, sell or share any data about you. Your expenses, categories, goals and Assistant chats are stored only in the app’s folder on your iPhone.",
"There are no ads, analytics, tracking or crash-reporting tools in the app. That’s why our App Store privacy label is “Data Not Collected”.",
]),
("What is stored on your device", [
"Expense records (amount, currency, merchant name, date, optional card label and note), categories and learned category rules, spending goals, feedback you give on insights, Assistant chat history and your app preferences.",
"A local diagnostics log helps you understand why an automation didn’t create a record. It never contains amounts, merchant names or card details — only whether each field arrived. It is kept for at most 7 days and can be turned off and cleared in Settings.",
"Data is stored with iOS file data protection and excluded from app backups (iCloud or computer). This means deleting the app also deletes your data.",
]),
("Apple Pay automation", [
"Sparios does not read your Wallet history or bank account. Records are created only when an automation you set up yourself in the Shortcuts app sends a payment to Sparios. You decide which cards are included.",
]),
("Assistant", [
"The Assistant uses Apple’s on-device language model (Apple Intelligence). Your questions and its answers never leave your iPhone and are not sent to any cloud AI service. The model cannot change or delete your expenses.",
]),
("Notifications", [
"All notifications are created on your device. Merchant names and amounts are not shown on the Lock Screen.",
]),
("Moving to another iPhone", [
"When you move your data to a new iPhone, the two devices connect directly over the local network or Bluetooth with end-to-end encryption. Your data never passes through a server. A transfer only starts after you enter the 6-digit code shown on the new iPhone.",
]),
("Purchases", [
"Sparios Pro subscriptions are processed entirely by Apple. Your payment details never reach us; the app only learns from Apple whether your subscription is active.",
]),
("Deleting your data", [
"Settings › Data management › <strong>Delete all my data</strong> permanently removes expenses, rules, goals, chats and scheduled notifications. Deleting the app removes all data as well.",
]),
("Children", [
"Sparios does not knowingly collect data from children — it doesn’t collect data from anyone.",
]),
("Changes and contact", [
"If this policy changes, the new date will appear on this page. Questions: <a href=\"mailto:{email}\">{email}</a>",
]),
],
"de": [
("Kurz gesagt", [
"Sparios verlangt kein Konto, verbindet sich mit keinem Server und erhebt, verkauft oder teilt keine Daten über dich. Deine Ausgaben, Kategorien, Ziele und Assistent-Chats werden ausschließlich im App-Ordner auf deinem iPhone gespeichert.",
"Die App enthält keine Werbung, keine Analyse-, Tracking- oder Absturzberichts-Tools. Deshalb lautet unser App-Store-Datenschutzetikett „Keine Daten erfasst“.",
]),
("Was auf deinem Gerät gespeichert wird", [
"Ausgaben (Betrag, Währung, Händlername, Datum, optionale Kartenbezeichnung und Notiz), Kategorien und gelernte Kategorieregeln, Ausgabenziele, dein Feedback zu Einblicken, der Assistent-Verlauf und deine App-Einstellungen.",
"Ein lokales Diagnoseprotokoll hilft dir zu verstehen, warum eine Automation keinen Eintrag erzeugt hat. Es enthält nie Beträge, Händlernamen oder Kartendaten – nur, ob ein Feld angekommen ist. Es wird höchstens 7 Tage aufbewahrt und kann in den Einstellungen ausgeschaltet und gelöscht werden.",
"Die Daten werden mit dem iOS-Datenschutz für Dateien gespeichert und von App-Backups (iCloud oder Computer) ausgeschlossen. Wenn du die App löschst, werden also auch deine Daten gelöscht.",
]),
("Apple-Pay-Automation", [
"Sparios liest weder deinen Wallet-Verlauf noch dein Bankkonto. Einträge entstehen nur, wenn eine Automation, die du selbst in der Kurzbefehle-App eingerichtet hast, eine Zahlung an Sparios übergibt. Du bestimmst, welche Karten dazugehören.",
]),
("Assistent", [
"Der Assistent nutzt Apples geräteinternes Sprachmodell (Apple Intelligence). Deine Fragen und die Antworten verlassen dein iPhone nicht und werden an keinen Cloud-KI-Dienst gesendet. Das Modell kann deine Ausgaben weder ändern noch löschen.",
]),
("Mitteilungen", [
"Alle Mitteilungen werden auf deinem Gerät erzeugt. Händlernamen und Beträge erscheinen nicht auf dem Sperrbildschirm.",
]),
("Umzug auf ein anderes iPhone", [
"Beim Übertragen deiner Daten auf ein neues iPhone verbinden sich beide Geräte direkt über das lokale Netzwerk oder Bluetooth, Ende-zu-Ende-verschlüsselt. Die Daten laufen über keinen Server. Die Übertragung startet erst, nachdem du den 6-stelligen Code vom neuen iPhone eingegeben hast.",
]),
("Käufe", [
"Das Sparios-Pro-Abo wird vollständig von Apple abgewickelt. Deine Zahlungsdaten erreichen uns nie; die App erfährt von Apple nur, ob dein Abo aktiv ist.",
]),
("Daten löschen", [
"Einstellungen › Datenverwaltung › <strong>Alle meine Daten löschen</strong> entfernt Ausgaben, Regeln, Ziele, Chats und geplante Mitteilungen dauerhaft. Auch das Löschen der App entfernt alle Daten.",
]),
("Kinder", [
"Sparios erhebt wissentlich keine Daten von Kindern – und auch von niemandem sonst.",
]),
("Änderungen und Kontakt", [
"Ändert sich diese Erklärung, steht das neue Datum auf dieser Seite. Fragen: <a href=\"mailto:{email}\">{email}</a>",
]),
],
},
"terms": {
"tr": [
("Genel", [
"Sparios’u App Store’dan indirerek <a href=\"{eula}\">Apple Standart Lisans Sözleşmesi (EULA)</a> kapsamında kullanırsın. Bu sayfa, o sözleşmeye ek olarak uygulamaya özgü birkaç noktayı açıklar.",
]),
("Sparios Pro aboneliği", [
"Sparios’un temel özellikleri ücretsizdir. Sparios Pro; Asistan, Pusula ay sonu tahminleri ve senaryolar, kişisel içgörüler ve akıllı bildirimleri açar. Aylık ve yıllık seçenekler vardır; güncel fiyatlar satın almadan önce uygulamada ve App Store’da gösterilir.",
"Ödeme, satın alma onayıyla Apple Kimliği hesabından alınır. Abonelik, mevcut dönem bitmeden en az 24 saat önce iptal edilmezse aynı süre ve fiyatla otomatik olarak yenilenir. Aboneliğini iPhone’unda Ayarlar › [adın] › Abonelikler bölümünden yönetebilir veya iptal edebilirsin. İptal, mevcut dönemin sonunda geçerli olur.",
"İade talepleri Apple tarafından değerlendirilir: <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>. İndirim ve teklif kodları App Store üzerinden kullanılır.",
]),
("Finansal tavsiye değildir", [
"Tahminler, içgörüler ve Asistan yanıtları yalnızca kendi kayıtlarından hesaplanan tahminlerdir. Eksik veya hatalı kayıtlar sonuçları etkiler. Sparios yatırım, vergi veya finansal danışmanlık sunmaz.",
]),
("Verilerin", [
"Veriler yalnızca cihazında tutulur ve uygulama yedeğine dahil edilmez. iPhone değiştirirken uygulamadaki aktarma özelliğini kullan; cihaz kaybında veya uygulama silindiğinde verileri geri getiremeyiz.",
]),
("Sorumluluk", [
"Uygulama “olduğu gibi” sunulur. Yasaların izin verdiği ölçüde, uygulamanın kullanımından doğan dolaylı zararlardan sorumlu değiliz. Tüketici olarak yasal haklarını etkilemez.",
]),
("İletişim", [
"<a href=\"mailto:{email}\">{email}</a>",
]),
],
"en": [
("General", [
"When you download Sparios from the App Store you use it under the <a href=\"{eula}\">Apple Standard Licensed Application End User License Agreement (EULA)</a>. This page adds a few points specific to the app.",
]),
("Sparios Pro subscription", [
"Sparios’s core features are free. Sparios Pro unlocks the Assistant, Compass end-of-month forecasts and scenarios, personal insights and smart notifications. Monthly and yearly options are available; current prices are shown in the app and on the App Store before you buy.",
"Payment is charged to your Apple Account at confirmation of purchase. The subscription renews automatically for the same period and price unless cancelled at least 24 hours before the end of the current period. You can manage or cancel it on your iPhone in Settings › [your name] › Subscriptions. Cancellation takes effect at the end of the current period.",
"Refunds are handled by Apple: <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>. Offer and discount codes are redeemed through the App Store.",
]),
("Not financial advice", [
"Forecasts, insights and Assistant answers are estimates calculated only from your own records. Missing or incorrect records affect the results. Sparios does not provide investment, tax or financial advice.",
]),
("Your data", [
"Your data is kept only on your device and is excluded from app backups. Use the in-app transfer when you switch iPhones; if a device is lost or the app is deleted, we cannot recover your data.",
]),
("Liability", [
"The app is provided “as is”. To the extent permitted by law, we are not liable for indirect damages arising from its use. This does not affect your statutory rights as a consumer.",
]),
("Contact", [
"<a href=\"mailto:{email}\">{email}</a>",
]),
],
"de": [
("Allgemeines", [
"Wenn du Sparios aus dem App Store lädst, nutzt du die App gemäß der <a href=\"{eula}\">Apple-Standard-Endbenutzer-Lizenzvereinbarung (EULA)</a>. Diese Seite ergänzt einige App-spezifische Punkte.",
]),
("Sparios-Pro-Abo", [
"Die Grundfunktionen von Sparios sind kostenlos. Sparios Pro schaltet den Assistenten, Kompass-Prognosen zum Monatsende und Szenarien, persönliche Einblicke und intelligente Mitteilungen frei. Es gibt ein Monats- und ein Jahresabo; die aktuellen Preise werden vor dem Kauf in der App und im App Store angezeigt.",
"Die Zahlung wird bei Kaufbestätigung über deinen Apple Account abgerechnet. Das Abo verlängert sich automatisch zum gleichen Zeitraum und Preis, sofern es nicht mindestens 24 Stunden vor Ende des laufenden Zeitraums gekündigt wird. Du kannst es auf deinem iPhone unter Einstellungen › [dein Name] › Abonnements verwalten oder kündigen. Die Kündigung wird zum Ende des laufenden Zeitraums wirksam.",
"Erstattungen wickelt Apple ab: <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>. Angebots- und Rabattcodes werden über den App Store eingelöst.",
]),
("Keine Finanzberatung", [
"Prognosen, Einblicke und Antworten des Assistenten sind Schätzungen, die nur aus deinen eigenen Einträgen berechnet werden. Fehlende oder falsche Einträge beeinflussen die Ergebnisse. Sparios bietet keine Anlage-, Steuer- oder Finanzberatung.",
]),
("Deine Daten", [
"Deine Daten liegen nur auf deinem Gerät und sind von App-Backups ausgeschlossen. Nutze beim iPhone-Wechsel die Übertragung in der App; bei Verlust des Geräts oder Löschen der App können wir deine Daten nicht wiederherstellen.",
]),
("Haftung", [
"Die App wird „wie besehen“ bereitgestellt. Soweit gesetzlich zulässig, haften wir nicht für mittelbare Schäden aus ihrer Nutzung. Deine gesetzlichen Verbraucherrechte bleiben unberührt.",
]),
("Kontakt", [
"<a href=\"mailto:{email}\">{email}</a>",
]),
],
},
"support": {
"tr": [
("Bize yaz", [
"Bir sorun mu var, yoksa bir fikrin mi? <a href=\"mailto:{email}\">{email}</a> adresine yaz; genellikle birkaç gün içinde yanıt veririz. iPhone modelini, iOS sürümünü ve Sparios sürümünü (Ayarlar › Hakkında) eklersen daha hızlı yardımcı olabiliriz.",
]),
("Apple Pay ödemelerim otomatik kaydedilmiyor", [
"Kurulumu Sparios’ta Ayarlar › Kurulum › Apple Pay otomasyonu rehberinden adım adım yapabilirsin. En sık üç neden:",
"<strong>1.</strong> Otomasyonda “Hemen çalıştır” kapalı. <strong>2.</strong> “Ne çalıştırılsın” ekranında “Yeni kestirme oluştur” yerine hazır “Harcama kaydet” kutucuğu seçilmiş; bu durumda tutar bağlanamaz. <strong>3.</strong> Tutar alanındaki “Kestirme Girdisi” balonuna dokunulup <em>Amount</em> seçilmemiş.",
"Kartını Cüzdan’dan kaldırıp yeniden eklediysen otomasyondaki kart seçimini yenile. Rehberin altındaki “Son otomasyon çağrısı” kartı, otomasyonun gerçekten çalışıp çalışmadığını gösterir.",
]),
("Aboneliğimi nasıl iptal ederim?", [
"iPhone’unda Ayarlar › [adın] › Abonelikler › Sparios Pro. İptal ettiğinde Pro, mevcut dönem bitene kadar açık kalır. Verilerin hiçbir durumda silinmez.",
]),
("Yeni iPhone’a geçtim, Pro görünmüyor", [
"Aynı Apple Kimliği ile giriş yaptığından emin ol, sonra Sparios’ta Ayarlar › Sparios Pro › <strong>Satın alımları geri yükle</strong>’ye dokun.",
]),
("İndirim kodumu nasıl kullanırım?", [
"Sparios’ta Ayarlar › Sparios Pro › <strong>İndirim kodu kullan</strong>’a dokun ve kodu Apple’ın açtığı ekrana gir. Kodlar App Store uygulamasındaki hesap sayfandan da kullanılabilir.",
]),
("Verilerimi yeni iPhone’a nasıl taşırım?", [
"İki iPhone’u yan yana koy ve ikisinde de Sparios’u aç. Yeni iPhone’da kurulum sırasında “Eski iPhone’dan aktar”ı seç; ekranda 6 haneli bir kod çıkar. Eski iPhone’da Ayarlar › Veri yönetimi › <strong>Başka iPhone’a aktar</strong>’a dokun, yeni cihazı seç ve kodu gir. Veriler iki cihaz arasında doğrudan ve şifreli aktarılır.",
"Aktarımdan sonra yeni iPhone’da Apple Pay otomasyonunu yeniden kurman gerekir; Kestirmeler otomasyonları cihazlar arasında taşınmaz.",
]),
("Asistan kullanılamıyor diyor", [
"Asistan, Apple Intelligence destekleyen bir iPhone’da iOS 26 veya sonrasını ve Ayarlar’da Apple Intelligence’ın açık olmasını gerektirir. Model ilk açılışta indirilirken bir süre beklemen gerekebilir.",
]),
("Tüm verilerimi nasıl silerim?", [
"Ayarlar › Veri yönetimi › <strong>Tüm verilerimi sil</strong>. Bu işlem geri alınamaz. Verilerin yalnızca cihazında olduğu için bizim tarafımızda silinecek bir kopya yoktur.",
]),
],
"en": [
("Write to us", [
"Found a problem or have an idea? Email <a href=\"mailto:{email}\">{email}</a> — we usually reply within a few days. Including your iPhone model, iOS version and Sparios version (Settings › About) helps us help you faster.",
]),
("My Apple Pay payments aren’t recorded automatically", [
"Follow the step-by-step guide in Sparios under Settings › Setup › Apple Pay automation. The three most common causes:",
"<strong>1.</strong> “Run Immediately” is off in the automation. <strong>2.</strong> On the “What should happen” screen the ready-made “Record expense” tile was picked instead of “Create New Shortcut”, so the amount can’t be connected. <strong>3.</strong> The “Shortcut Input” bubble in the Amount field wasn’t tapped to choose <em>Amount</em>.",
"If you removed and re-added your card in Wallet, re-select it in the automation. The “Last automation call” card under the guide shows whether the automation actually ran.",
]),
("How do I cancel my subscription?", [
"On your iPhone go to Settings › [your name] › Subscriptions › Sparios Pro. After cancelling, Pro stays active until the current period ends. Your data is never deleted.",
]),
("I switched iPhones and Pro isn’t showing", [
"Make sure you’re signed in with the same Apple Account, then in Sparios tap Settings › Sparios Pro › <strong>Restore Purchases</strong>.",
]),
("How do I redeem an offer code?", [
"In Sparios tap Settings › Sparios Pro › <strong>Redeem code</strong> and enter the code on the screen Apple shows. You can also redeem codes from your account page in the App Store app.",
]),
("How do I move my data to a new iPhone?", [
"Place both iPhones next to each other and open Sparios on both. On the new iPhone, choose “Transfer from old iPhone” during setup; a 6-digit code appears. On the old iPhone tap Settings › Data management › <strong>Transfer to another iPhone</strong>, pick the new device and enter the code. Your data moves directly and encrypted between the two devices.",
"After the transfer, set up the Apple Pay automation again on the new iPhone — Shortcuts automations don’t move between devices.",
]),
("The Assistant says it’s unavailable", [
"The Assistant needs an iPhone that supports Apple Intelligence, iOS 26 or later, and Apple Intelligence turned on in Settings. The model may take a while to download the first time.",
]),
("How do I delete all my data?", [
"Settings › Data management › <strong>Delete all my data</strong>. This can’t be undone. Because your data only exists on your device, there is no copy on our side to delete.",
]),
],
"de": [
("Schreib uns", [
"Ein Problem oder eine Idee? Schreib an <a href=\"mailto:{email}\">{email}</a> – wir antworten meist innerhalb weniger Tage. Mit iPhone-Modell, iOS-Version und Sparios-Version (Einstellungen › Über) können wir schneller helfen.",
]),
("Meine Apple-Pay-Zahlungen werden nicht automatisch erfasst", [
"Folge der Schritt-für-Schritt-Anleitung in Sparios unter Einstellungen › Einrichtung › Apple-Pay-Automation. Die drei häufigsten Ursachen:",
"<strong>1.</strong> „Sofort ausführen“ ist in der Automation ausgeschaltet. <strong>2.</strong> Auf dem Bildschirm „Was soll ausgeführt werden“ wurde die fertige Kachel „Ausgabe erfassen“ statt „Neuen Kurzbefehl erstellen“ gewählt – dann lässt sich der Betrag nicht verbinden. <strong>3.</strong> Im Feld „Betrag“ wurde nicht auf die Blase „Kurzbefehleingabe“ getippt und <em>Amount</em> gewählt.",
"Wenn du deine Karte aus Wallet entfernt und neu hinzugefügt hast, wähle sie in der Automation erneut aus. Die Karte „Letzter Automationsaufruf“ unter der Anleitung zeigt, ob die Automation wirklich gelaufen ist.",
]),
("Wie kündige ich mein Abo?", [
"Auf dem iPhone: Einstellungen › [dein Name] › Abonnements › Sparios Pro. Nach der Kündigung bleibt Pro bis zum Ende des laufenden Zeitraums aktiv. Deine Daten werden nie gelöscht.",
]),
("Neues iPhone – Pro wird nicht angezeigt", [
"Stelle sicher, dass du mit demselben Apple Account angemeldet bist, und tippe in Sparios auf Einstellungen › Sparios Pro › <strong>Käufe wiederherstellen</strong>.",
]),
("Wie löse ich einen Angebotscode ein?", [
"Tippe in Sparios auf Einstellungen › Sparios Pro › <strong>Code einlösen</strong> und gib den Code im Apple-Fenster ein. Codes lassen sich auch über deine Accountseite in der App-Store-App einlösen.",
]),
("Wie übertrage ich meine Daten auf ein neues iPhone?", [
"Lege beide iPhones nebeneinander und öffne auf beiden Sparios. Wähle auf dem neuen iPhone bei der Einrichtung „Vom alten iPhone übertragen“; ein 6-stelliger Code erscheint. Tippe auf dem alten iPhone auf Einstellungen › Datenverwaltung › <strong>Auf anderes iPhone übertragen</strong>, wähle das neue Gerät und gib den Code ein. Die Daten werden direkt und verschlüsselt zwischen beiden Geräten übertragen.",
"Richte danach die Apple-Pay-Automation auf dem neuen iPhone neu ein – Kurzbefehle-Automationen werden nicht zwischen Geräten übertragen.",
]),
("Der Assistent ist nicht verfügbar", [
"Der Assistent benötigt ein iPhone mit Apple Intelligence, iOS 26 oder neuer und eingeschaltete Apple Intelligence in den Einstellungen. Beim ersten Mal kann das Laden des Modells etwas dauern.",
]),
("Wie lösche ich alle meine Daten?", [
"Einstellungen › Datenverwaltung › <strong>Alle meine Daten löschen</strong>. Das lässt sich nicht rückgängig machen. Da deine Daten nur auf deinem Gerät liegen, gibt es bei uns keine Kopie zu löschen.",
]),
],
},
"accessibility": {
"tr": [
("Hedefimiz", [
"Sparios’u görme, işitme, motor veya bilişsel farklılığı olan herkesin rahatça kullanabilmesini istiyoruz.",
]),
("Desteklenenler", [
"<strong>VoiceOver:</strong> Tüm düğmeler, grafikler ve kartlar anlamlı etiketler taşır; grafiklerin değerleri ayrıca liste olarak okunur.",
"<strong>Dinamik Yazı:</strong> Metinler en büyük erişilebilirlik boyutlarına kadar büyür ve kesilmeden alt satıra geçer.",
"<strong>Koyu Görünüm ve kontrast:</strong> Açık ve koyu temada metin renkleri okunabilir kontrast için seçilmiştir; artış/azalış yalnızca renkle değil ok ve kelimeyle de belirtilir.",
"<strong>Hareketi Azalt:</strong> Bu ayar açıkken animasyonlar sadeleşir.",
"<strong>Dokunma alanları:</strong> Etkileşimli öğeler en az 44 × 44 pt’dir.",
]),
("Bir engelle mi karşılaştın?", [
"Bize <a href=\"mailto:{email}\">{email}</a> adresinden yaz; kullandığın yardımcı teknolojiyi ve ekranı belirtirsen önceliklendirerek düzeltiriz.",
]),
],
"en": [
("Our goal", [
"We want everyone — including people with visual, hearing, motor or cognitive disabilities — to use Sparios comfortably.",
]),
("What’s supported", [
"<strong>VoiceOver:</strong> Buttons, charts and cards carry meaningful labels; chart values are also available as a readable list.",
"<strong>Dynamic Type:</strong> Text scales up to the largest accessibility sizes and wraps instead of being cut off.",
"<strong>Dark Mode and contrast:</strong> Text colors are chosen for legible contrast in light and dark; increases and decreases are shown with arrows and words, not color alone.",
"<strong>Reduce Motion:</strong> Animations are simplified when this setting is on.",
"<strong>Touch targets:</strong> Interactive elements are at least 44 × 44 pt.",
]),
("Ran into a barrier?", [
"Email <a href=\"mailto:{email}\">{email}</a>. Tell us which assistive technology and screen you were using and we’ll prioritise a fix.",
]),
],
"de": [
("Unser Ziel", [
"Alle sollen Sparios bequem nutzen können – auch Menschen mit Seh-, Hör-, motorischen oder kognitiven Einschränkungen.",
]),
("Unterstützt", [
"<strong>VoiceOver:</strong> Tasten, Diagramme und Karten haben aussagekräftige Beschriftungen; Diagrammwerte gibt es zusätzlich als lesbare Liste.",
"<strong>Dynamische Schrift:</strong> Texte wachsen bis zu den größten Bedienungshilfen-Größen und brechen um, statt abgeschnitten zu werden.",
"<strong>Dunkelmodus und Kontrast:</strong> Textfarben sind in hell und dunkel auf gute Lesbarkeit abgestimmt; Anstieg und Rückgang werden mit Pfeilen und Worten gezeigt, nicht nur mit Farbe.",
"<strong>Bewegung reduzieren:</strong> Ist die Einstellung aktiv, werden Animationen vereinfacht.",
"<strong>Tippflächen:</strong> Bedienelemente sind mindestens 44 × 44 pt groß.",
]),
("Auf eine Barriere gestoßen?", [
"Schreib an <a href=\"mailto:{email}\">{email}</a>. Nenne die genutzte Hilfstechnologie und den Bildschirm – wir beheben es mit Priorität.",
]),
],
},
}

CSS = """
:root{--bg:#F8F6F0;--surface:#FFFEF9;--ink:#233D32;--muted:#646C62;--accent:#2F654E;--soft:#E9EEE0;--line:#E4E4D9}
@media (prefers-color-scheme:dark){:root{--bg:#1B211E;--surface:#252D27;--ink:#EDF2E9;--muted:#ADB7AA;--accent:#A7D3B2;--soft:#2D3C2C;--line:#3C473C}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 -apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Arial,sans-serif;padding-inline:20px}
.wrap{max-width:680px;margin:0 auto;padding-block:28px 56px}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:36px}
.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font:500 20px/1 ui-serif,"New York",Georgia,serif}
.mark{width:34px;height:34px;border-radius:10px;background:var(--accent);color:var(--bg);display:grid;place-items:center;font:600 18px/1 ui-serif,Georgia,serif}
nav.langs{display:flex;gap:4px;font-size:13px}
nav.langs a{color:var(--muted);text-decoration:none;padding:5px 9px;border-radius:999px}
nav.langs a[aria-current]{background:var(--soft);color:var(--accent);font-weight:600}
h1{font:500 clamp(30px,6vw,40px)/1.15 ui-serif,"New York",Georgia,serif;margin:0 0 10px;text-wrap:balance}
.lede{color:var(--muted);font-size:18px;margin:0 0 8px}
.updated{color:var(--muted);font-size:13px;letter-spacing:.02em;margin:0 0 32px}
section{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:20px 22px;margin-bottom:14px}
h2{font:500 21px/1.3 ui-serif,"New York",Georgia,serif;margin:0 0 8px}
p{margin:0 0 10px}p:last-child{margin-bottom:0}
a{color:var(--accent);text-underline-offset:3px}
a:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:28px}
.card{display:block;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:18px 20px}
.card strong{display:block;font:500 19px/1.3 ui-serif,Georgia,serif;margin-bottom:4px}
.card span{color:var(--muted);font-size:14px}
.back{display:inline-block;margin-bottom:18px;font-size:14px;text-decoration:none}
footer{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:18px}
footer nav{display:flex;flex-wrap:wrap;gap:6px 16px;margin-bottom:10px}
footer a{color:var(--muted)}
"""


def page(lang, slug, title, body, description):
    ui = UI[lang]
    rel = "../" if slug else ""
    root = "../../" if slug else "../"
    langs = "".join(
        f'<a href="{root}{l}/{slug + "/" if slug else ""}" hreflang="{l}" lang="{l}"'
        + (' aria-current="true"' if l == lang else "") + f">{l.upper()}</a>"
        for l in LANGS
    )
    alternates = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{root}{l}/{slug + "/" if slug else ""}">' for l in LANGS
    )
    foot_links = "".join(f'<a href="{rel}{p}/">{ui[p]}</a>' for p in PAGES)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="color-scheme" content="light dark">
{alternates}
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<div class="wrap">
<header>
<a class="brand" href="{rel or './'}"><span class="mark" aria-hidden="true">S</span>Sparios</a>
<nav class="langs" aria-label="{ui['lang']}">{langs}</nav>
</header>
<main>
{body}
</main>
<footer>
<nav>{foot_links}</nav>
<p>{html.escape(ui['footer'])}</p>
</footer>
</div>
</body>
</html>
"""


def fill(text):
    return text.replace("{email}", EMAIL).replace("{eula}", EULA)


def build():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    open(os.path.join(OUT, "style.css"), "w").write(CSS.strip() + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    for lang in LANGS:
        ui = UI[lang]
        cards = "".join(
            f'<a class="card" href="{p}/"><strong>{ui[p]}</strong><span>{html.escape(SUMMARY[p][lang])}</span></a>'
            for p in PAGES
        )
        home = f'<h1>Sparios</h1><p class="lede">{html.escape(ui["tagline"])}</p><p>{html.escape(ui["intro"])}</p><div class="cards">{cards}</div>'
        os.makedirs(os.path.join(OUT, lang), exist_ok=True)
        open(os.path.join(OUT, lang, "index.html"), "w").write(page(lang, "", "Sparios", home, ui["tagline"]))
        for slug in PAGES:
            sections = "".join(
                f"<section><h2>{html.escape(h)}</h2>" + "".join(f"<p>{fill(p)}</p>" for p in paras) + "</section>"
                for h, paras in CONTENT[slug][lang]
            )
            body = (f'<a class="back" href="../">← {ui["home"]}</a><h1>{ui[slug]}</h1>'
                    f'<p class="lede">{html.escape(SUMMARY[slug][lang])}</p>'
                    f'<p class="updated">{ui["updated"]}: {UPDATED[lang]}</p>{sections}')
            os.makedirs(os.path.join(OUT, lang, slug), exist_ok=True)
            open(os.path.join(OUT, lang, slug, "index.html"), "w").write(
                page(lang, slug, f"{ui[slug]} · Sparios", body, SUMMARY[slug][lang]))
    # Root: pick the visitor's language, with plain links as the no-JS fallback.
    root = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Sparios</title><meta name="color-scheme" content="light dark"><link rel="stylesheet" href="style.css">
<script>(function(){var l=(navigator.language||'en').slice(0,2).toLowerCase();location.replace((['tr','de'].indexOf(l)>=0?l:'en')+'/');})();</script></head>
<body><div class="wrap"><h1>Sparios</h1><div class="cards"><a class="card" href="tr/"><strong>Türkçe</strong></a><a class="card" href="en/"><strong>English</strong></a><a class="card" href="de/"><strong>Deutsch</strong></a></div></div></body></html>
"""
    open(os.path.join(OUT, "index.html"), "w").write(root)
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")


if __name__ == "__main__":
    build()
