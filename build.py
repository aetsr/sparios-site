#!/usr/bin/env python3
"""Builds the static Sparios legal & support site (TR/EN/DE) into docs/ for GitHub Pages.

Only public web copy lives in this repository — no app source code.
Run: python3 build.py
"""
import html
import os
import shutil

OUT = "docs"
EMAIL = "spariosapp@gmail.com"
UPDATED = {"tr": "16 Ekim 2026", "en": "16 October 2026", "de": "16. Oktober 2026"}
LANGS = ["tr", "en", "de"]
PAGES = ["privacy", "terms", "support", "accessibility"]
EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"

UI = {
    "tr": {
        "home": "Ana sayfa", "privacy": "Gizlilik", "terms": "Kullanım Koşulları", "support": "Destek",
        "accessibility": "Erişilebilirlik", "updated": "Son güncelleme", "contact": "İletişim",
        "tagline": "Harcamalarını cihazında tutan, sakin bir harcama defteri.",
        "intro": "Bankanın uygulaması yalnız kendi kartını gösterir. Sparios, Apple Pay’de hangi kartla ödersen öde harcamanı kaydeder; kiran, faturaların ve elle girdiklerin de yanında durur. Hepsi yalnızca iPhone’unda kalır. Hesap yok, sunucu yok, reklam yok.",
        "footer": "Sparios bağımsız bir geliştirici tarafından yapılmıştır. Apple, Apple Pay ve iPhone, Apple Inc.’in ticari markalarıdır.",
        "lang": "Dil",
    },
    "en": {
        "home": "Home", "privacy": "Privacy", "terms": "Terms of Use", "support": "Support",
        "accessibility": "Accessibility", "updated": "Last updated", "contact": "Contact",
        "tagline": "A calm spending journal that keeps your data on your device.",
        "intro": "Your bank’s app only shows its own card. Sparios records your Apple Pay spending whichever card you pay with, right next to your rent, bills and anything you add by hand. It all stays on your iPhone. No account, no server, no ads.",
        "footer": "Sparios is made by an independent developer. Apple, Apple Pay and iPhone are trademarks of Apple Inc.",
        "lang": "Language",
    },
    "de": {
        "home": "Start", "privacy": "Datenschutz", "terms": "Nutzungsbedingungen", "support": "Support",
        "accessibility": "Barrierefreiheit", "updated": "Zuletzt aktualisiert", "contact": "Kontakt",
        "tagline": "Ein ruhiges Ausgabenbuch, das deine Daten auf deinem Gerät lässt.",
        "intro": "Die App deiner Bank zeigt nur ihre eigene Karte. Sparios erfasst deine Apple-Pay-Ausgaben, egal mit welcher Karte du zahlst, gleich neben Miete, Rechnungen und deinen eigenen Einträgen. Alles bleibt auf deinem iPhone. Kein Konto, kein Server, keine Werbung.",
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
        "tr": "Uygulamayı hangi koşullarla kullandığın.",
        "en": "The terms for using the app.",
        "de": "Die Bedingungen für die Nutzung der App.",
    },
    "support": {
        "tr": "Apple Pay kurulumu, cihaz değiştirme ve sık sorulanlar.",
        "en": "Automation setup, switching iPhones and common questions.",
        "de": "Automations-Einrichtung, iPhone-Wechsel und häufige Fragen.",
    },
    "accessibility": {
        "tr": "Sparios’u herkesin rahatça kullanabilmesi için neler yaptık.",
        "en": "What we do so everyone can use Sparios comfortably.",
        "de": "Was wir tun, damit alle Sparios bequem nutzen können.",
    },
}

# Page bodies: list of (heading, [paragraph html, ...]). Inline <strong>/<a> allowed.
# Set once the app is live: the App Store link the home page's button points to.
APP_STORE_URL = None
# A plain link only: no Buy Me a Coffee widget script, so the site stays free of third-party code.
COFFEE_URL = "https://www.buymeacoffee.com/sparios"

HOME = {
    "en": {
        "title": "Sparios · A spending journal that fills itself in",
        "hero": "Tap to pay.<br>Sparios writes it down.",
        "sub": "A spending journal that fills itself in. Pay with any card in your Wallet and see what’s left this month. No bank login, no account, nothing leaves your iPhone.",
        "soon": "Coming soon to the App Store", "get": "Free on the App Store",
        "trust": ["Free", "No account", "No tracking"],
        "gallery": "A look inside", "prev": "Previous", "next": "Next",
        "cards_title": "Everything your month needs. Nothing it doesn’t.",
        "cards": [
            ("card", "Every payment, already written down", "Set up one Shortcuts automation and every Apple Pay payment lands in Sparios a moment later. Rent, bills and cash go in the same list."),
            ("wallet", "Know what’s left", "Add your income once. Rent and subscriptions are booked on their day, and you always see what’s left and your daily share."),
            ("compass", "See the month-end coming", "Compass shows where this month is heading. Each evening Sparios draws its own line. Stay under it and you win the month."),
            ("chat", "Ask about your money", "“How much did I spend on groceries this month?” The Assistant answers from your own entries, on your iPhone."),
            ("office", "A tiny office", "Five pixel colleagues bring in your receipts, file them and work out your month-end. Tap one to see what they’re up to."),
            ("bell", "Quiet by design", "At most one notification a day, in the evening. Nothing at night. Pick a category right from the notification."),
        ],
        "private": "Your money stays yours.",
        "points": ["No account. No bank login.", "No tracking, no ads, no data collection.", "Online only for exchange rates, and only if you turn it on."],
        "free": "Free. No subscription.",
        "help": "Questions? See support",
        "coffee": "Enjoying Sparios? Buy me a coffee",
        "coffee_short": "Buy me a coffee",
        "shot": "Sparios on iPhone",
    },
    "tr": {
        "title": "Sparios · Kendi kendine dolan harcama defteri",
        "hero": "Öde.<br>Sparios not alsın.",
        "sub": "Kendi kendine dolan bir harcama defteri. Wallet’taki hangi kartla ödersen öde, bu ay ne kaldığını gör. Banka girişi yok, hesap yok, hiçbir şey iPhone’undan çıkmaz.",
        "soon": "Yakında App Store’da", "get": "App Store’da ücretsiz",
        "trust": ["Ücretsiz", "Hesap yok", "Takip yok"],
        "gallery": "İçeriden bir bakış", "prev": "Önceki", "next": "Sonraki",
        "cards_title": "Ayın için gereken her şey. Fazlası değil.",
        "cards": [
            ("card", "Her ödeme zaten yazılı", "Kestirmeler’de bir kez otomasyon kur; her Apple Pay ödemen birkaç saniyede Sparios’a düşsün. Kira, fatura ve nakit de aynı listede."),
            ("wallet", "Ne kaldığını bil", "Gelirini bir kez ekle. Kira ve abonelikler günü gelince düşer; ne kaldığını ve günlük payını hep görürsün."),
            ("compass", "Ay sonunu önceden gör", "Pusula ayın nereye gittiğini gösterir. Sparios her akşam kendi çizgisini çizer. Altında kalırsan ayı sen kazanırsın."),
            ("chat", "Paranı sor", "“Bu ay markete ne kadar harcadım?” Asistan kendi kayıtlarından, iPhone’unda cevap verir."),
            ("office", "Küçük bir ofis", "Beş piksel çalışan fişlerini getirir, dosyalar ve ay sonunu hesaplar. Ne yaptıklarını görmek için birine dokun."),
            ("bell", "Sessiz tasarım", "Günde en fazla bir bildirim, akşam. Gece hiçbir şey yok. Kategoriyi bildirimden seçersin."),
        ],
        "private": "Paran sende kalır.",
        "points": ["Hesap yok. Banka girişi yok.", "Takip yok, reklam yok, veri toplama yok.", "İnternete yalnız kur için çıkar, o da sen açarsan."],
        "free": "Ücretsiz. Abonelik yok.",
        "help": "Sorun mu var? Destek sayfası",
        "coffee": "Sparios işine yaradıysa bir kahve ısmarla",
        "coffee_short": "Bir kahve ısmarla",
        "shot": "iPhone’da Sparios",
    },
    "de": {
        "title": "Sparios · Ein Ausgabenbuch, das sich selbst füllt",
        "hero": "Bezahlen.<br>Sparios schreibt mit.",
        "sub": "Ein Ausgabenbuch, das sich selbst füllt. Zahl mit jeder Karte aus deinem Wallet und sieh, was diesen Monat übrig ist. Kein Bank-Login, kein Konto, nichts verlässt dein iPhone.",
        "soon": "Bald im App Store", "get": "Kostenlos im App Store",
        "trust": ["Kostenlos", "Kein Konto", "Kein Tracking"],
        "gallery": "Ein Blick hinein", "prev": "Zurück", "next": "Weiter",
        "cards_title": "Alles, was dein Monat braucht. Nichts darüber hinaus.",
        "cards": [
            ("card", "Jede Zahlung, schon eingetragen", "Richte einmal eine Kurzbefehle-Automation ein, und jede Apple-Pay-Zahlung landet Sekunden später in Sparios. Miete, Rechnungen und Bargeld stehen in derselben Liste."),
            ("wallet", "Wissen, was übrig ist", "Trag dein Einkommen einmal ein. Miete und Abos werden an ihrem Tag gebucht, und du siehst immer, was übrig ist."),
            ("compass", "Das Monatsende kommen sehen", "Der Kompass zeigt, wohin dein Monat steuert. Jeden Abend zieht Sparios seine eigene Linie. Bleib darunter, und der Monat gehört dir."),
            ("chat", "Frag nach deinem Geld", "„Wie viel habe ich diesen Monat für Lebensmittel ausgegeben?“ Der Assistent antwortet aus deinen Einträgen, auf dem iPhone."),
            ("office", "Ein kleines Büro", "Fünf Pixel-Kollegen bringen deine Belege, legen sie ab und rechnen dein Monatsende. Tipp jemanden an und sieh, was gerade passiert."),
            ("bell", "Ruhig gebaut", "Höchstens eine Mitteilung am Tag, abends. Nachts nichts. Die Kategorie wählst du direkt in der Mitteilung."),
        ],
        "private": "Dein Geld bleibt bei dir.",
        "points": ["Kein Konto. Kein Bank-Login.", "Kein Tracking, keine Werbung, keine Datenerhebung.", "Online nur für Wechselkurse, und nur wenn du es einschaltest."],
        "free": "Kostenlos. Kein Abo.",
        "help": "Fragen? Zum Support",
        "coffee": "Gefällt dir Sparios? Spendier mir einen Kaffee",
        "coffee_short": "Spendier mir einen Kaffee",
        "shot": "Sparios auf dem iPhone",
    },
}

GALLERY = ["panorama-1", "panorama-2", "store-14-office", "store-09-radar", "store-12-assistant", "store-11-outlook", "store-04-race", "store-13-receipt"]

ICONS = {
    "card": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3 10h18M7 15h4"/>',
    "wallet": '<rect x="3" y="7" width="18" height="12" rx="3"/><path d="M6 7V6a1 1 0 0 1 1-1h10v2"/><circle cx="16.5" cy="13" r="1.2"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "chat": '<path d="M5 5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-8l-4 3v-3H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/>',
    "office": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M10 21v-4h4v4"/>',
    "bell": '<path d="M6 16v-5a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
}


def icon(name):
    return (f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

SUPPORT_UI = {
    "tr": {"coffee": "Sparios işine yaradıysa bir kahve ısmarlayabilirsin", "write": "Bize yaz", "faq": "Sık sorulanlar", "reply": "Genellikle birkaç gün içinde yanıt veririz. iPhone modelini, iOS ve Sparios sürümünü (Ayarlar › Hakkında) eklersen daha hızlı yardımcı olabiliriz."},
    "en": {"coffee": "Enjoying Sparios? You can buy me a coffee", "write": "Write to us", "faq": "Common questions", "reply": "We usually reply within a few days. Adding your iPhone model, iOS version and Sparios version (Settings › About) helps us help you faster."},
    "de": {"coffee": "Gefällt dir Sparios? Du kannst mir einen Kaffee spendieren", "write": "Schreib uns", "faq": "Häufige Fragen", "reply": "Wir antworten meist innerhalb weniger Tage. Mit iPhone-Modell, iOS- und Sparios-Version (Einstellungen › Über) können wir schneller helfen."},
}

CONTENT = {
"privacy": {
"tr": [
("Kısaca", [
"Sparios bir hesap istemez, kendi sunucusu yoktur ve senin hakkında hiçbir veri toplamaz, satmaz ya da paylaşmaz. Harcamaların, gelirlerin, bütçen, hedeflerin ve Asistan sohbetlerin yalnızca iPhone’undaki uygulama klasöründe saklanır. Tek istisna, senin açabileceğin döviz kuru indirmesidir (aşağıda); o da hiçbir veri göndermez.",
"Uygulamada reklam, analiz, izleme veya çökme raporlama aracı yoktur. App Store gizlilik etiketimiz bu yüzden “Veri Toplanmaz”dır.",
]),
("Cihazında saklananlar", [
"Harcama kayıtları (tutar, para birimi, işletme adı, tarih, isteğe bağlı kart etiketi ve not), gelirler, sabit ödemeler, birikim hedefleri ve döviz kurları, kategoriler ve öğrenilen kategori kuralları, harcama hedefleri, içgörülere verdiğin geri bildirimler, Asistan sohbet geçmişi ve uygulama tercihlerin.",
"Otomasyonun neden kayıt oluşturmadığını anlamana yardım eden yerel bir tanılama günlüğü tutulur. Bu günlük tutar, işletme adı veya kart bilgisi içermez; yalnızca alanların gelip gelmediğini kaydeder, en fazla 7 gün saklanır ve Ayarlar’dan kapatılıp temizlenebilir.",
"Veriler iOS dosya veri korumasıyla saklanır ve uygulama yedeğinden (iCloud/bilgisayar yedeği) hariç tutulur. Bu, uygulamayı silersen verilerin de silineceği anlamına gelir.",
]),
("Apple Pay otomasyonu", [
"Sparios, Cüzdan geçmişini veya banka hesabını okumaz. Kayıtlar yalnızca senin Kestirmeler uygulamasında kendin kurduğun otomasyon Sparios’a bir ödeme gönderdiğinde oluşur. Hangi kartların izleneceğine sen karar verirsin.",
]),
("Döviz kurları", [
"Bütçen başka para birimindeki gelir ve giderleri ana birimine çevirmek için kur kullanır. Kuru kendin girebilirsin ya da <strong>isteğe bağlı</strong> olarak indirmeyi açabilirsin. İndirme varsayılan olarak kapalıdır; yalnız tek bir para birimi kullanıyorsan Sparios hiç internete çıkmaz.",
"Açarsan Sparios günde en fazla bir kez Avrupa Merkez Bankası’nın herkese açık günlük kur tablosunu indirir. Bu istekle hiçbir veri gönderilmez: hesap, cihaz kimliği ya da harcama/gelir bilgisi yoktur. Her web isteğinde olduğu gibi iPhone’unun IP adresi bankanın sunucusuna ulaşır; Sparios bu isteği görmez ve kaydetmez. Ayarlar › Para birimi ve kur’dan dilediğin an kapatabilirsin.",
]),
("Asistan", [
"Asistan sorularını iPhone’unda anlar ve cevapları yalnızca kendi kayıtlarından hesaplar. Apple Intelligence destekleyen cihazlarda, cevabın cümleleri Apple’ın cihaz içi dil modeliyle daha doğal hâle getirilebilir. Soruların ve yanıtlar iPhone’undan çıkmaz; hiçbir bulut yapay zekâ hizmetine gönderilmez. Asistan harcamalarını değiştiremez veya silemez.",
]),
("Bildirimler", [
"Tüm bildirimler cihazında, uygulamanın kendisi tarafından oluşturulur. Push sunucusu, cihaz jetonu ya da uzak bildirim yoktur; hiçbir bildirim için verin cihazdan çıkmaz.",
"Bildirim metni, yararlı olabilmesi için tutar, işletme adı ya da kategori içerebilir — örneğin kategori bekleyen bir kaydı doğrudan bildirimden işaretleyebilmen için. <strong>Kilit ekranında ne görüneceğini sen belirlersin:</strong> iOS Ayarlar › Bildirimler › Sparios › Önizlemeleri Göster tercihini “Kilitliyken değil” ya da “Asla” yaptığında Sparios kilit ekranında yalnız kısa bir yer tutucu gösterir (“Gözden geçirilecek kayıt var” gibi); tutar ve işletme adı görünmez.",
"Bildirim izni kurulumun sonunda bir kez istenir ve istemezsen uygulama bildirim göndermez. Uygulama içi Ayarlar › Bildirimler’den dilediğin an kapatabilir ve bildirim saatini değiştirebilirsin. Gece 22:00–09:00 arası bildirim gelmez.",
]),
("Başka bir iPhone’a aktarma", [
"Verilerini yeni iPhone’una taşımak istediğinde iki cihaz yerel ağ veya Bluetooth üzerinden, uçtan uca şifreli ve doğrudan birbirine bağlanır. Veriler hiçbir sunucudan geçmez. Bağlantıyı yalnızca yeni iPhone’da gösterilen 10 karakterlik kodu girerek başlatabilirsin; iki telefon da kodu bildiğini kanıtlamadan veri gitmez.",
]),
("Verilerini silmek", [
"Ayarlar › Veri yönetimi › <strong>Tüm verilerimi sil</strong> harcamaları, kuralları, hedefleri, sohbetleri ve planlanmış bildirimleri kalıcı olarak siler. Uygulamayı silmek de tüm verileri kaldırır.",
]),
("Şifreli yedek", [
"Ayarlar › Veri yönetimi › Yedek ile bir yedek dosyası oluşturabilirsin. Dosya, seçtiğin şifreyle cihazında şifrelenir ve senin seçtiğin yere kaydedilir (ör. iCloud Drive). Bize gönderilmez; şifren olmadan biz de açamayız. Şifreni unutursan yedek açılamaz.",
]),
("Bu web sitesi", [
"Kahve linkine tıklarsan Buy Me a Coffee’nin sitesine gidersin; orada onların gizlilik kuralları geçerli. Bu sitede onlara ait bir kod yok.",
"Bu site GitHub Pages’te barındırılır. Bir sayfayı açtığında GitHub, sayfayı sunmak ve güvenliği sağlamak için IP adresini ve teknik istek bilgilerini işler. Sitede çerez, analiz ya da takip yok; bu kayıtlar bize ulaşmaz. Hukuki dayanak: siteyi sunmaktaki meşru menfaat (GDPR md. 6/1-f). Ayrıntılar: <a href=\"https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement\">GitHub gizlilik bildirimi</a>.",
"Bize e-posta yazarsan adresini ve mesajını yalnızca sana cevap vermek için kullanırız.",
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
"Sparios doesn’t ask for an account, has no server of its own, and doesn’t collect, sell or share any data about you. Your expenses, income, budget, goals and Assistant chats are stored only in the app’s folder on your iPhone. The one exception is the exchange-rate download you can choose to turn on (below), and it sends no data.",
"There are no ads, analytics, tracking or crash-reporting tools in the app. That’s why our App Store privacy label is “Data Not Collected”.",
]),
("What is stored on your device", [
"Expense records (amount, currency, merchant name, date, optional card label and note), income, fixed payments, savings goals and exchange rates, categories and learned category rules, spending goals, feedback you give on insights, Assistant chat history and your app preferences.",
"A local diagnostics log helps you understand why an automation didn’t create a record. It never contains amounts, merchant names or card details — only whether each field arrived. It is kept for at most 7 days and can be turned off and cleared in Settings.",
"Data is stored with iOS file data protection and excluded from app backups (iCloud or computer). This means deleting the app also deletes your data.",
]),
("Apple Pay automation", [
"Sparios does not read your Wallet history or bank account. Records are created only when an automation you set up yourself in the Shortcuts app sends a payment to Sparios. You decide which cards are included.",
]),
("Exchange rates", [
"Your budget uses exchange rates to convert income and expenses in other currencies into your main currency. You can enter a rate yourself or <strong>choose</strong> to turn on downloading. Downloading is off by default; if you only use one currency, Sparios never goes online.",
"If you turn it on, Sparios downloads the European Central Bank’s public daily reference-rate table at most once a day. No data is sent with this request: no account, no device identifier and no spending or income information. As with any web request, your iPhone’s IP address reaches the bank’s server; Sparios doesn’t see or store this request. You can turn it off at any time in Settings › Currency and rates.",
]),
("Assistant", [
"The Assistant understands your questions on your iPhone and calculates answers only from your own entries. On devices that support Apple Intelligence, Apple’s on-device language model may make the wording more natural. Your questions and its answers never leave your iPhone and are not sent to any cloud AI service. The Assistant cannot change or delete your expenses.",
]),
("Notifications", [
"All notifications are created on your device, by the app itself. There is no push server, no device token and no remote notification; no notification causes your data to leave the device.",
"To be useful, a notification’s text may contain an amount, a merchant name or a category — for example so you can categorize a waiting entry straight from the notification. <strong>You decide what appears on the Lock Screen:</strong> set iOS Settings › Notifications › Sparios › Show Previews to “When Unlocked” or “Never” and Sparios shows only a short placeholder there (such as “You have entries to review”); no amount and no merchant name.",
"Notification permission is asked once, at the end of setup, and the app sends nothing if you decline. You can turn notifications off at any time in the app’s Settings › Notifications, and change the delivery time. Nothing is delivered between 22:00 and 09:00.",
]),
("Moving to another iPhone", [
"When you move your data to a new iPhone, the two devices connect directly over the local network or Bluetooth with end-to-end encryption. Your data never passes through a server. A transfer only starts after you enter the 10-character code shown on the new iPhone, and no data moves until both phones have proven they know it.",
]),
("Deleting your data", [
"Settings › Data management › <strong>Delete all my data</strong> permanently removes expenses, rules, goals, chats and scheduled notifications. Deleting the app removes all data as well.",
]),
("Encrypted backup", [
"In Settings › Data management › Backup you can create a backup file. It is encrypted on your device with a password you choose and saved where you choose (for example iCloud Drive). It is never sent to us, and without your password we can’t open it either. If you forget the password, the backup can’t be opened.",
]),
("This website", [
"If you follow the coffee link, you go to Buy Me a Coffee’s website, where their privacy policy applies. This site contains none of their code.",
"This website is hosted on GitHub Pages. When you open a page, GitHub processes your IP address and technical request data to deliver the page and keep the service secure. There are no cookies, analytics or tracking on this site, and we don’t receive these logs. Legal basis: our legitimate interest in providing the website (Art. 6(1)(f) GDPR). Details: <a href=\"https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement\">GitHub’s privacy statement</a>.",
"If you email us, we use your address and message only to answer you.",
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
"Sparios verlangt kein Konto, hat keinen eigenen Server und erhebt, verkauft oder teilt keine Daten über dich. Deine Ausgaben, Einnahmen, dein Budget, deine Ziele und Assistent-Chats werden ausschließlich im App-Ordner auf deinem iPhone gespeichert. Einzige Ausnahme ist der Wechselkurs-Download, den du einschalten kannst (unten) – er sendet keine Daten.",
"Die App enthält keine Werbung, keine Analyse-, Tracking- oder Absturzberichts-Tools. Deshalb lautet unser App-Store-Datenschutzetikett „Keine Daten erfasst“.",
]),
("Was auf deinem Gerät gespeichert wird", [
"Ausgaben (Betrag, Währung, Händlername, Datum, optionale Kartenbezeichnung und Notiz), Einnahmen, Fixkosten, Sparziele und Wechselkurse, Kategorien und gelernte Kategorieregeln, Ausgabenziele, dein Feedback zu Einblicken, der Assistent-Verlauf und deine App-Einstellungen.",
"Ein lokales Diagnoseprotokoll hilft dir zu verstehen, warum eine Automation keinen Eintrag erzeugt hat. Es enthält nie Beträge, Händlernamen oder Kartendaten – nur, ob ein Feld angekommen ist. Es wird höchstens 7 Tage aufbewahrt und kann in den Einstellungen ausgeschaltet und gelöscht werden.",
"Die Daten werden mit dem iOS-Datenschutz für Dateien gespeichert und von App-Backups (iCloud oder Computer) ausgeschlossen. Wenn du die App löschst, werden also auch deine Daten gelöscht.",
]),
("Apple-Pay-Automation", [
"Sparios liest weder deinen Wallet-Verlauf noch dein Bankkonto. Einträge entstehen nur, wenn eine Automation, die du selbst in der Kurzbefehle-App eingerichtet hast, eine Zahlung an Sparios übergibt. Du bestimmst, welche Karten dazugehören.",
]),
("Wechselkurse", [
"Dein Budget nutzt Wechselkurse, um Einnahmen und Ausgaben in anderen Währungen in deine Hauptwährung umzurechnen. Du kannst einen Kurs selbst eingeben oder den Download <strong>freiwillig</strong> einschalten. Der Download ist standardmäßig aus; nutzt du nur eine Währung, geht Sparios nie online.",
"Schaltest du ihn ein, lädt Sparios höchstens einmal täglich die öffentliche Tabelle der Referenzkurse der Europäischen Zentralbank. Mit dieser Anfrage werden keine Daten gesendet: kein Konto, keine Gerätekennung, keine Ausgaben- oder Einnahmendaten. Wie bei jeder Webanfrage erreicht die IP-Adresse deines iPhones den Server der Bank; Sparios sieht und speichert diese Anfrage nicht. Du kannst ihn jederzeit unter Einstellungen › Währung und Kurse ausschalten.",
]),
("Assistent", [
"Der Assistent versteht deine Fragen auf deinem iPhone und berechnet die Antworten nur aus deinen eigenen Einträgen. Auf Geräten mit Apple Intelligence kann Apples geräteinternes Sprachmodell die Formulierung natürlicher machen. Deine Fragen und die Antworten verlassen dein iPhone nicht und werden an keinen Cloud-KI-Dienst gesendet. Der Assistent kann deine Ausgaben weder ändern noch löschen.",
]),
("Mitteilungen", [
"Alle Mitteilungen werden auf deinem Gerät von der App selbst erzeugt. Es gibt keinen Push-Server, kein Gerätetoken und keine Remote-Mitteilungen; für keine Mitteilung verlassen deine Daten das Gerät.",
"Damit eine Mitteilung nützlich ist, kann ihr Text einen Betrag, einen Händlernamen oder eine Kategorie enthalten – etwa damit du einen wartenden Eintrag direkt aus der Mitteilung heraus zuordnen kannst. <strong>Was auf dem Sperrbildschirm erscheint, bestimmst du:</strong> Stellst du in iOS Einstellungen › Mitteilungen › Sparios › Vorschau zeigen auf „Wenn entsperrt“ oder „Nie“, zeigt Sparios dort nur einen kurzen Platzhalter (etwa „Du hast Einträge zum Durchsehen“); weder Betrag noch Händlername.",
"Die Mitteilungsberechtigung wird einmal am Ende der Einrichtung erfragt; lehnst du ab, sendet die App nichts. In den App-Einstellungen › Mitteilungen kannst du sie jederzeit abschalten und dort die Zustellzeit ändern. Zwischen 22:00 und 09:00 wird nichts zugestellt.",
]),
("Umzug auf ein anderes iPhone", [
"Beim Übertragen deiner Daten auf ein neues iPhone verbinden sich beide Geräte direkt über das lokale Netzwerk oder Bluetooth, Ende-zu-Ende-verschlüsselt. Die Daten laufen über keinen Server. Die Übertragung startet erst, nachdem du den 10-stelligen Code vom neuen iPhone eingegeben hast; Daten fließen erst, wenn beide Geräte den Code nachgewiesen haben.",
]),
("Daten löschen", [
"Einstellungen › Datenverwaltung › <strong>Alle meine Daten löschen</strong> entfernt Ausgaben, Regeln, Ziele, Chats und geplante Mitteilungen dauerhaft. Auch das Löschen der App entfernt alle Daten.",
]),
("Verschlüsseltes Backup", [
"Unter Einstellungen › Datenverwaltung › Backup kannst du eine Backup-Datei erstellen. Sie wird auf deinem Gerät mit einem Passwort deiner Wahl verschlüsselt und dort gespeichert, wo du es festlegst (z. B. iCloud Drive). Sie wird nie an uns gesendet; ohne dein Passwort können auch wir sie nicht öffnen. Vergisst du das Passwort, lässt sich das Backup nicht öffnen.",
]),
("Diese Website", [
"Folgst du dem Kaffee-Link, gelangst du zu Buy Me a Coffee; dort gilt deren Datenschutzerklärung. Diese Website enthält keinen Code von ihnen.",
"Diese Website wird bei GitHub Pages gehostet. Beim Aufruf einer Seite verarbeitet GitHub deine IP-Adresse und technische Anfragedaten, um die Seite auszuliefern und den Dienst zu sichern. Auf dieser Website gibt es keine Cookies, keine Analyse und kein Tracking, und diese Protokolle erreichen uns nicht. Rechtsgrundlage: unser berechtigtes Interesse an der Bereitstellung der Website (Art. 6 Abs. 1 lit. f DSGVO). Details: <a href=\"https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement\">Datenschutzerklärung von GitHub</a>.",
"Wenn du uns eine E-Mail schreibst, verwenden wir deine Adresse und Nachricht nur, um dir zu antworten.",
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
("Finansal tavsiye değildir", [
"Tahminler, içgörüler ve Asistan yanıtları yalnızca kendi kayıtlarından hesaplanan tahminlerdir. Eksik veya hatalı kayıtlar sonuçları etkiler. Sparios yatırım, vergi veya finansal danışmanlık sunmaz.",
]),
("Verilerin", [
"Veriler yalnızca cihazında tutulur ve uygulama yedeğine dahil edilmez. iPhone değiştirirken uygulamadaki aktarmayı kullan ya da kendi şifreli yedeğini al (Ayarlar › Veri yönetimi › Yedek). Yedeğin yoksa, cihaz kaybında veya uygulama silindiğinde verileri geri getiremeyiz.",
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
("Not financial advice", [
"Forecasts, insights and Assistant answers are estimates calculated only from your own records. Missing or incorrect records affect the results. Sparios does not provide investment, tax or financial advice.",
]),
("Your data", [
"Your data is kept only on your device and is excluded from app backups. Use the in-app transfer when you switch iPhones, or keep your own encrypted backup (Settings › Data management › Backup). Without one, if a device is lost or the app is deleted, we cannot recover your data.",
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
("Keine Finanzberatung", [
"Prognosen, Einblicke und Antworten des Assistenten sind Schätzungen, die nur aus deinen eigenen Einträgen berechnet werden. Fehlende oder falsche Einträge beeinflussen die Ergebnisse. Sparios bietet keine Anlage-, Steuer- oder Finanzberatung.",
]),
("Deine Daten", [
"Deine Daten liegen nur auf deinem Gerät und sind von App-Backups ausgeschlossen. Nutze beim iPhone-Wechsel die Übertragung in der App oder leg dir ein eigenes verschlüsseltes Backup an (Einstellungen › Datenverwaltung › Backup). Ohne Backup können wir deine Daten bei Verlust des Geräts oder Löschen der App nicht wiederherstellen.",
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
"Kurulum Sparios’ta Ayarlar › Apple Pay otomasyonu’nda. Hazır kestirmeyi ekler, otomasyonu açarsın. Yalnız temassız Apple Pay ödemeleri kaydolur; online ve fiziksel kart ödemeleri sayılmaz.",
"<strong>iOS 27:</strong> Kestirmeler › Otomasyon listesinde Sparios otomasyonunun anahtarı açık olsun; eklenince kapalı gelir. <strong>iOS 26 ve öncesi:</strong> otomasyonda ödediğin kartlar işaretli ve “Hemen Çalıştır” seçili olsun.",
"Ayarlar › Apple Pay otomasyonu’ndaki “Son otomasyon çağrısı” otomasyonun Sparios’a ulaşıp ulaşmadığını gösterir. Hâlâ gelmiyorsa aynı sayfadaki “Elle kur”u dene.",
]),
("Verilerimi yeni iPhone’a nasıl taşırım?", [
"İki iPhone’u yan yana koy ve ikisinde de Sparios’u aç. Yeni iPhone’da kurulum sırasında “Eski iPhone’dan aktar”ı (ya da Ayarlar › Veri yönetimi › Cihaz aktarımı › “Bu yeni iPhone’um”) seç; ekranda 10 karakterlik bir kod çıkar. Eski iPhone’da Ayarlar › Veri yönetimi › <strong>Cihaz aktarımı</strong> › “Bu eski iPhone’um”a dokun, yeni cihazı seç ve kodu gir. Veriler iki cihaz arasında doğrudan ve şifreli aktarılır.",
"Aktarımdan sonra yeni iPhone’da Apple Pay otomasyonunu yeniden kurman gerekir; Kestirmeler otomasyonları cihazlar arasında taşınmaz.",
]),
("Asistan hangi cihazlarda çalışır?", [
"Asistan, Sparios’u çalıştıran her iPhone’da çalışır; cevaplar anında ve cihazında hesaplanır. Apple Intelligence destekleyen ve açık olan bir iPhone’da (iOS 26 veya sonrası) cevapların cümleleri ek olarak daha doğal hâle getirilir.",
]),
("Widget'ları nasıl eklerim?", [
"Ana ekranda boş bir yere basılı tut, sol üstteki <strong>+</strong> düğmesine dokun ve listeden Sparios'u seç. Sekiz widget vardır: kalan bütçe (ana ekranda ve kilit ekranında), ay sonu tahmini, “Sparios'u yen” yarışı, bu ayın kategori dağılımı, bu hafta, bütçe ve yaklaşan ödemeler, birikim hedefi ve kilit ekranı bütçe göstergesi. Widget'lar uygulamanın hesapladığı değerleri gösterir; bir Apple Pay ödemesi kaydedildiğinde ve uygulamayı açtığında güncellenir.",
]),
("Sparios bana ne zaman bildirim gönderir?", [
"Sparios her gün açılan bir uygulama değil, o yüzden bildirimleri de seyrektir. Gönderilenler günde tek bir akşam penceresinde toplanır (varsayılan 20:30) ve 22:00–09:00 arasında hiçbir şey gelmez. Herhangi bir hafta içinde en fazla iki harcama içgörüsü gönderilir; hafta/ay kapanışları ve “kısayol kayıt göndermiyor” uyarısı bu sayının dışındadır.",
"Ayarlar › Bildirimler’de tek bir seçim yaparsın: <strong>Sadece önemli olduğunda</strong>, <strong>Önemli + haftalık özet</strong> ya da <strong>Kapalı</strong>. Aynı ekranda bildirim saatini değiştirebilirsin; gece 22:00–09:00 arası bildirim gelmez.",
"Bir kayıt kategori bekliyorsa bildirime uzun basıp kategoriyi doğrudan oradan seçebilirsin; uygulamayı açman gerekmez.",
]),
("Kilit ekranımda tutar ve işletme adı görünsün istemiyorum", [
"iPhone’unda Ayarlar › Bildirimler › Sparios › <strong>Önizlemeleri Göster</strong> ayarını “Kilitliyken değil” ya da “Asla” yap. Sparios bu durumda kilit ekranında yalnız kısa bir yer tutucu gösterir (“Gözden geçirilecek kayıt var” gibi); tutar, işletme adı ve kategori görünmez. Telefonun kilidini açtığında bildirimin tam metni yerinde durur.",
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
"Setup lives in Sparios under Settings › Apple Pay automation: you add a ready-made shortcut and switch its automation on. Only contactless Apple Pay payments are recorded; online and physical-card payments are not.",
"<strong>iOS 27:</strong> in Shortcuts › Automation, the Sparios automation must be switched on; it arrives switched off. <strong>iOS 26 and earlier:</strong> the cards you pay with must be ticked and “Run Immediately” chosen.",
"“Last automation call” in Settings › Apple Pay automation shows whether the automation reached Sparios. If nothing arrives, try “Set it up by hand” on the same page.",
]),
("How do I move my data to a new iPhone?", [
"Place both iPhones next to each other and open Sparios on both. On the new iPhone, choose “Transfer from old iPhone” during setup (or Settings › Data management › Device transfer › “This is my new iPhone”); a 10-character code appears. On the old iPhone tap Settings › Data management › <strong>Device transfer</strong> › “This is my old iPhone”, pick the new device and enter the code. Your data moves directly and encrypted between the two devices.",
"After the transfer, set up the Apple Pay automation again on the new iPhone — Shortcuts automations don’t move between devices.",
]),
("Which devices does the Assistant work on?", [
"The Assistant works on every iPhone that runs Sparios; answers are calculated instantly on your device. On an iPhone with Apple Intelligence turned on (iOS 26 or later), the wording of answers is additionally made more natural.",
]),
("How do I add the widgets?", [
"Touch and hold an empty spot on your Home Screen, tap <strong>+</strong> in the top left and pick Sparios. There are eight widgets: budget left (on the Home Screen and the Lock Screen), month-end forecast, the “Beat Sparios” race, this month by category, this week, budget with upcoming payments, savings goal and a Lock Screen budget gauge. Widgets show the figures the app calculated; they refresh when an Apple Pay payment is recorded and when you open the app.",
]),
("When does Sparios send me notifications?", [
"Sparios isn’t an app you open every day, so its notifications are sparse too. Whatever there is gets collected into one evening window a day (20:30 by default), and nothing arrives between 22:00 and 09:00. At most two spending insights are sent in any week; the week and month closings and the “the shortcut has stopped delivering entries” warning don’t count towards that.",
"In Settings › Notifications you make one choice: <strong>Only when it matters</strong>, <strong>Important + weekly summary</strong>, or <strong>Off</strong>. The same screen lets you change the delivery time; nothing is delivered between 22:00 and 09:00.",
"If an entry is waiting for a category, long-press the notification and pick the category right there — no need to open the app.",
]),
("I don’t want amounts and merchant names on my Lock Screen", [
"On your iPhone, set Settings › Notifications › Sparios › <strong>Show Previews</strong> to “When Unlocked” or “Never”. Sparios then shows only a short placeholder on the Lock Screen (such as “You have entries to review”); no amount, merchant name or category. Once you unlock the phone, the notification’s full text is there.",
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
"Die Einrichtung findest du in Sparios unter Einstellungen › Apple-Pay-Automation: Du fügst einen fertigen Kurzbefehl hinzu und schaltest seine Automation ein. Erfasst werden nur kontaktlose Apple-Pay-Zahlungen, nicht Online- oder Kartenzahlungen.",
"<strong>iOS 27:</strong> In Kurzbefehle › Automation muss die Sparios-Automation eingeschaltet sein; nach dem Hinzufügen ist sie aus. <strong>iOS 26 und älter:</strong> Deine Karten müssen angehakt und „Sofort ausführen“ gewählt sein.",
"„Letzter Automationsaufruf“ unter Einstellungen › Apple-Pay-Automation zeigt, ob die Automation Sparios erreicht hat. Kommt weiter nichts an, probier auf derselben Seite „Selbst einrichten“.",
]),
("Wie übertrage ich meine Daten auf ein neues iPhone?", [
"Lege beide iPhones nebeneinander und öffne auf beiden Sparios. Wähle auf dem neuen iPhone bei der Einrichtung „Vom alten iPhone übertragen“ (oder Einstellungen › Datenverwaltung › Geräteübertragung › „Das ist mein neues iPhone“); ein 10-stelliger Code erscheint. Tippe auf dem alten iPhone auf Einstellungen › Datenverwaltung › <strong>Geräteübertragung</strong> › „Das ist mein altes iPhone“, wähle das neue Gerät und gib den Code ein. Die Daten werden direkt und verschlüsselt zwischen beiden Geräten übertragen.",
"Richte danach die Apple-Pay-Automation auf dem neuen iPhone neu ein – Kurzbefehle-Automationen werden nicht zwischen Geräten übertragen.",
]),
("Auf welchen Geräten funktioniert der Assistent?", [
"Der Assistent funktioniert auf jedem iPhone, auf dem Sparios läuft; Antworten werden sofort auf dem Gerät berechnet. Auf einem iPhone mit eingeschalteter Apple Intelligence (iOS 26 oder neuer) wird die Formulierung zusätzlich natürlicher.",
]),
("Wie füge ich die Widgets hinzu?", [
"Halte eine freie Stelle auf dem Home-Bildschirm gedrückt, tippe oben links auf <strong>+</strong> und wähle Sparios. Es gibt acht Widgets: Restbudget (auf dem Home-Bildschirm und dem Sperrbildschirm), Prognose zum Monatsende, das Rennen „Sparios schlagen“, dieser Monat nach Kategorien, diese Woche, Budget mit anstehenden Zahlungen, Sparziel und eine Budgetanzeige für den Sperrbildschirm. Die Widgets zeigen die von der App berechneten Werte; sie aktualisieren sich, wenn eine Apple-Pay-Zahlung erfasst wird und wenn du die App öffnest.",
]),
("Wann schickt mir Sparios Mitteilungen?", [
"Sparios ist keine App, die man täglich öffnet – entsprechend selten sind auch die Mitteilungen. Was anfällt, wird in einem Abendfenster pro Tag gebündelt (standardmäßig 20:30), und zwischen 22:00 und 09:00 kommt nichts. Pro Woche werden höchstens zwei Ausgaben-Einblicke gesendet; die Wochen- und Monatsabschlüsse und die Warnung „der Kurzbefehl liefert keine Einträge mehr“ zählen nicht dazu.",
"Unter Einstellungen › Mitteilungen triffst du eine einzige Wahl: <strong>Nur wenn es wichtig ist</strong>, <strong>Wichtiges + Wochenübersicht</strong> oder <strong>Aus</strong>. Auf demselben Bildschirm änderst du die Zustellzeit; zwischen 22:00 und 09:00 wird nichts zugestellt.",
"Wartet ein Eintrag auf eine Kategorie, drückst du lange auf die Mitteilung und wählst die Kategorie direkt dort – die App musst du dafür nicht öffnen.",
]),
("Ich möchte keine Beträge und Händlernamen auf meinem Sperrbildschirm", [
"Stelle auf deinem iPhone Einstellungen › Mitteilungen › Sparios › <strong>Vorschau zeigen</strong> auf „Wenn entsperrt“ oder „Nie“. Sparios zeigt dann auf dem Sperrbildschirm nur einen kurzen Platzhalter (etwa „Du hast Einträge zum Durchsehen“); weder Betrag noch Händlername oder Kategorie. Nach dem Entsperren steht der vollständige Text der Mitteilung wie gewohnt da.",
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
:root{--bg:#F8F6F0;--surface:#FFFEF9;--ink:#1F3A2E;--muted:#5E675D;--accent:#2F654E;--accent-ink:#FFFEF9;--soft:#E9EEE0;--line:#E2E3D7;--night:#14281F;--night-ink:#EAF2EA;--night-muted:#A9BFAE;--bezel:#121614}
@media (prefers-color-scheme:dark){:root{--bg:#161C19;--surface:#202823;--ink:#EDF2E9;--muted:#A7B2A4;--accent:#A7D3B2;--accent-ink:#13261C;--soft:#26332A;--line:#34403A;--night:#0F1E17;--night-ink:#EAF2EA;--night-muted:#9FB6A4;--bezel:#000}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Arial,sans-serif}
.serif,h1,h2,h3,.brand{font-family:ui-serif,"New York",Georgia,serif;font-weight:500}
.wrap{max-width:720px;margin:0 auto;padding:0 20px}
.wide{max-width:1080px}
header.top{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding-block:22px}
.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-size:21px}
.brand img{width:34px;height:34px;border-radius:9px}
nav.langs{display:flex;gap:4px;font-size:13px}
nav.langs a{color:var(--muted);text-decoration:none;padding:5px 10px;border-radius:999px}
nav.langs a[aria-current]{background:var(--soft);color:var(--accent);font-weight:600}
h1{font-size:clamp(32px,6vw,44px);line-height:1.12;margin:8px 0 12px;text-wrap:balance}
h2{font-size:22px;line-height:1.3;margin:0 0 8px}
.lede{color:var(--muted);font-size:18px;margin:0 0 8px}
.updated{color:var(--muted);font-size:13px;letter-spacing:.02em;margin:0 0 28px}
section.box{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:20px 22px;margin-bottom:14px}
p{margin:0 0 10px}p:last-child{margin-bottom:0}
a{color:var(--accent);text-underline-offset:3px}
a:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:6px}
.back{display:inline-block;margin:6px 0 14px;font-size:14px;text-decoration:none}
/* Home */
body.home{background:var(--bg)}
.stage{background:linear-gradient(100deg,#183428 0%,#22463a 45%,#36624a 100%);color:#FAF8EE;border-radius:0 0 40px 40px;overflow:hidden}
.stage header.top .brand{color:#FAF8EE}
.stage nav.langs a{color:rgba(250,248,238,.7)}
.stage nav.langs a[aria-current]{background:rgba(250,248,238,.14);color:#FAF8EE}
.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:24px;align-items:center;padding-block:24px 0}
.hero .copy{padding-bottom:64px}
.hero h1{font-size:clamp(44px,6.6vw,80px);line-height:1;letter-spacing:-.025em;margin:0 0 22px;color:#FAF8EE}
.hero .sub{font-size:19px;line-height:1.55;color:rgba(250,248,238,.78);max-width:31em;margin:0 0 28px}
.pill{display:inline-flex;align-items:center;gap:10px;padding:14px 22px;border-radius:999px;background:#FAF8EE;color:#183428;font-weight:600;text-decoration:none;font-size:16px}
.pill svg{width:18px;height:18px}
.pill.soon{background:rgba(250,248,238,.12);color:#FAF8EE;border:1px solid rgba(250,248,238,.25)}
.ctas{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.pill.coffee-hero{background:#FFDD00;color:#1b1b1b;border:0;box-shadow:0 10px 24px -12px rgba(255,221,0,.6)}
.pill.coffee-hero:hover{filter:brightness(1.03)}
.trust{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:22px;font-size:14px;color:rgba(250,248,238,.7);list-style:none;padding:0}
.trust li::before{content:"✓";margin-right:6px;color:#B9DEC2}
.hero .art{align-self:end;display:flex;justify-content:center}
.hero .art img{width:100%;max-width:470px;height:auto;display:block;margin-bottom:-6px}
.eyebrow{font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0 0 10px}
.gallery-wrap{padding-block:72px 24px}
.gallery-wrap h2,.cards-wrap h2{font-size:clamp(28px,4vw,42px);line-height:1.1;letter-spacing:-.015em;margin:0 0 28px;max-width:20em}
body.home{overflow-x:clip}
.gal-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:28px}
.gal-head h2{margin:0!important}
.gal-nav{display:flex;gap:8px;flex:none}
.gal-nav button{width:46px;height:46px;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:500 22px/1 -apple-system,sans-serif;cursor:pointer;display:grid;place-items:center;transition:opacity .2s,transform .15s}
.gal-nav button:hover:not(:disabled){transform:scale(1.06)}
.gal-nav button:disabled{opacity:.3;cursor:default}
.gal-nav button:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
/* Full-bleed strip: starts in line with the heading, runs to the window's edge, fades out there. */
.gallery{--edge:max(20px,calc((100vw - 1080px)/2 + 20px));display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px var(--edge) 20px;scroll-padding-inline:var(--edge);margin-inline:calc(50% - 50vw);scrollbar-width:none;-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 72px),transparent);mask-image:linear-gradient(90deg,#000 calc(100% - 72px),transparent)}
.gallery.at-end{-webkit-mask-image:none;mask-image:none}
@media (hover:none){.gal-nav{display:none}}
.gallery::-webkit-scrollbar{display:none}
.gallery img{flex:0 0 auto;width:240px;height:auto;border-radius:22px;scroll-snap-align:start;box-shadow:0 18px 40px -22px rgba(20,40,30,.45)}
.gallery img.pair{border-radius:22px 0 0 22px}.gallery img.pair2{border-radius:0 22px 22px 0;margin-left:-16px}
.cards-wrap{padding-block:56px 24px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.fcard{background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:26px 24px}
.fcard .ic{width:46px;height:46px;border-radius:14px;display:grid;place-items:center;background:var(--soft);color:var(--accent);margin-bottom:18px}
.fcard h3{font-family:ui-serif,"New York",Georgia,serif;font-weight:500;font-size:22px;line-height:1.2;margin:0 0 8px}
.fcard p{color:var(--muted);font-size:16px;margin:0}
.band{background:linear-gradient(100deg,#183428,#2b5240);color:#FAF8EE;border-radius:32px;padding:52px 44px;margin-block:56px 24px;display:grid;grid-template-columns:.9fr 1.1fr;gap:32px;align-items:center}
.band h2{font-size:clamp(32px,4.6vw,48px);line-height:1.05;letter-spacing:-.02em;margin:0}
.band .lockic{width:52px;height:52px;border-radius:16px;display:grid;place-items:center;background:rgba(250,248,238,.12);margin-bottom:18px}
.band ul{list-style:none;padding:0;margin:0;display:grid;gap:12px}
.band li{background:rgba(250,248,238,.07);border:1px solid rgba(250,248,238,.12);border-radius:16px;padding:14px 18px;color:rgba(250,248,238,.88);font-size:17px}
.closing{text-align:center;padding-block:40px 16px}
.closing h2{font-size:clamp(30px,4.4vw,46px);letter-spacing:-.02em;margin:0 0 18px}
.closing .pill{background:var(--accent);color:var(--accent-ink)}
.closing .pill.soon{background:var(--soft);color:var(--accent);border:0}
.closing p{margin-top:16px}
.coffee{display:inline-flex;align-items:center;gap:6px;padding:10px 16px;border-radius:999px;background:var(--soft);color:var(--accent);text-decoration:none;font-weight:600;font-size:15px}
.coffee:hover{filter:brightness(.97)}
.coffee-line{margin:-12px 0 28px}
/* Support */
.contact{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;background:var(--night);color:var(--night-ink);border-radius:22px;padding:22px 24px;margin-bottom:28px}
.contact h2{margin:0 0 4px}.contact p{color:var(--night-muted);margin:0}
.contact .pill{background:var(--night-ink);color:var(--night)}
details{background:var(--surface);border:1px solid var(--line);border-radius:16px;margin-bottom:10px}
summary{cursor:pointer;list-style:none;padding:16px 48px 16px 20px;position:relative;font-family:ui-serif,"New York",Georgia,serif;font-size:19px;line-height:1.35}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:20px;top:14px;font:400 22px/1 -apple-system,sans-serif;color:var(--accent)}
details[open] summary::after{content:"–"}
details .a{padding:0 20px 18px}
h3.faq{font-size:15px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-family:-apple-system,sans-serif;font-weight:600;margin:0 0 12px}
footer{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-block:20px 40px}
footer nav{display:flex;flex-wrap:wrap;gap:6px 16px;margin-bottom:10px}
footer a{color:var(--muted)}
@media (max-width:860px){
.grid{grid-template-columns:1fr 1fr}
.band{grid-template-columns:1fr;padding:36px 26px}
}
@media (max-width:640px){
.hero{grid-template-columns:1fr;gap:0;padding-top:4px}
.hero .copy{padding-bottom:28px}
.hero .art img{max-width:340px}
.grid{grid-template-columns:1fr}
.gallery img{width:200px}
.stage{border-radius:0 0 28px 28px}
.band{border-radius:24px}
}
"""


def page(lang, slug, title, body, description, stage=None):
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
    header = (f'<header class="top"><a class="brand" href="{rel or "./"}"><img src="{root}assets/icon-192.png" alt="">Sparios</a>'
              f'<nav class="langs" aria-label="{ui["lang"]}">{langs}</nav></header>')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="color-scheme" content="light dark">
{'<meta name="theme-color" content="#183428">' if stage else ''}
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="https://aetsr.github.io/sparios-site/assets/icon-512.png">
<link rel="icon" href="{root}assets/favicon.png">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
{alternates}
<link rel="stylesheet" href="{root}style.css">
</head>
<body{' class="home"' if stage else ''}>
{f'<div class="stage"><div class="wrap wide">{header}{stage}</div></div>' if stage else ''}
<div class="wrap{' wide' if stage else ''}">
{'' if stage else header}
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
    shutil.copytree("assets", os.path.join(OUT, "assets"))
    for lang in LANGS:
        ui = UI[lang]
        h = HOME[lang]
        apple = ""
        def button(extra=""):
            return (f'<a class="pill{extra}" href="{APP_STORE_URL}">{apple}{h["get"]}</a>' if APP_STORE_URL
                    else f'<span class="pill soon{extra}">{apple}{h["soon"]}</span>')
        trust = "".join(f"<li>{html.escape(t)}</li>" for t in h["trust"])
        stage = (f'<section class="hero"><div class="copy"><h1>{h["hero"]}</h1><p class="sub">{html.escape(h["sub"])}</p>'
                 f'<div class="ctas">{button()}<a class="pill coffee-hero" href="{COFFEE_URL}" rel="noopener">☕ {html.escape(h["coffee_short"])}</a></div>'
                 f'<ul class="trust">{trust}</ul></div>'
                 f'<div class="art"><img src="../assets/{lang}/hero.webp" width="960" height="1144" alt="{html.escape(h["shot"])}"></div></section>')
        shots = "".join(
            f'<img src="../assets/{lang}/{g}.jpg" width="560" height="1217" loading="lazy" alt="{html.escape(h["shot"])}"'
            + (' class="pair"' if g == "panorama-1" else ' class="pair2"' if g == "panorama-2" else "") + ">"
            for g in GALLERY
        )
        cards = "".join(
            f'<article class="fcard"><div class="ic">{icon(k)}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>'
            for k, t, d in h["cards"]
        )
        points = "".join(f"<li>{html.escape(x)}</li>" for x in h["points"])
        nav = (f'<div class="gal-nav"><button type="button" class="gal-prev" aria-label="{html.escape(h["prev"])}">‹</button>'
               f'<button type="button" class="gal-next" aria-label="{html.escape(h["next"])}">›</button></div>')
        # Own inline script, no third-party code: arrow buttons for mouse users, disabled at the ends.
        gal_js = ("<script>(function(){var g=document.querySelector('.gallery'),p=document.querySelector('.gal-prev'),n=document.querySelector('.gal-next');"
                  "if(!g||!p||!n)return;function s(){return Math.max(g.clientWidth*.8,260)}"
                  "p.onclick=function(){g.scrollBy({left:-s(),behavior:'smooth'})};n.onclick=function(){g.scrollBy({left:s(),behavior:'smooth'})};"
                  "function u(){var e=g.scrollLeft+g.clientWidth>=g.scrollWidth-4;p.disabled=g.scrollLeft<4;n.disabled=e;g.classList.toggle('at-end',e)}"
                  "g.addEventListener('scroll',u,{passive:true});addEventListener('resize',u);u()})();</script>")
        home = (f'<section class="gallery-wrap"><p class="eyebrow">Sparios</p><div class="gal-head"><h2>{html.escape(h["gallery"])}</h2>{nav}</div><div class="gallery" tabindex="0">{shots}</div>{gal_js}</section>'
                f'<section class="cards-wrap"><h2>{html.escape(h["cards_title"])}</h2><div class="grid">{cards}</div></section>'
                f'<section class="band"><div><div class="lockic">{icon("lock")}</div><h2>{html.escape(h["private"])}</h2></div><ul>{points}</ul></section>'
                f'<section class="closing"><h2>{html.escape(h["free"])}</h2>{button()}<p><a href="support/">{html.escape(h["help"])} →</a></p>'
                f'<p><a class="coffee" href="{COFFEE_URL}" rel="noopener">☕ {html.escape(h["coffee"])}</a></p></section>')
        os.makedirs(os.path.join(OUT, lang), exist_ok=True)
        open(os.path.join(OUT, lang, "index.html"), "w").write(page(lang, "", h["title"], home, h["sub"], stage=stage))
        for slug in PAGES:
            if slug == "support":
                su = SUPPORT_UI[lang]
                questions = "".join(
                    f"<details><summary>{html.escape(q)}</summary><div class=\"a\">" + "".join(f"<p>{fill(p)}</p>" for p in paras) + "</div></details>"
                    for q, paras in CONTENT[slug][lang][1:]
                )
                sections = (f'<div class="contact"><div><h2>{su["write"]}</h2><p>{su["reply"]}</p></div>'
                            f'<a class="pill" href="mailto:{EMAIL}">{EMAIL}</a></div>'
                            f'<p class="coffee-line"><a class="coffee" href="{COFFEE_URL}" rel="noopener">☕ {html.escape(su["coffee"])}</a></p>'
                            f'<h3 class="faq">{su["faq"]}</h3>{questions}')
            else:
                sections = "".join(
                    f'<section class="box"><h2>{html.escape(h)}</h2>' + "".join(f"<p>{fill(p)}</p>" for p in paras) + "</section>"
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
