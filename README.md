Name : Faatir Wibowo Rachmad

NPM : 2506595146

Class :   PBP C

### Tugas 1
1. iya, saya menggunakan elemen semantik HTML5 yaitu seperti <header>
 <nav>,<main>,<section>, <article>, dan <footer>. elemen elemen ini bantu buat membagi bagi setiap halaman sesuai fungsi fungsinya. misalnya kalo <header> itu untuk navigasi, <section> niat bagian profil, pengalaman, pendidikan, dll. elemen elemen ini bikin kode saya lebih rapih dan gampang dipahami. 

 2. Tantangan utama yang saya alami adalah pas tampilan di desktop kan banyak kolomnya, pas di mobile jadi terlalu sempit. agar tidak terlalu sempit, pada ukuran layar maksimal 768px saya merubah layoutnya jadi satu kolom aja. terus kalo buat yang pendidikan kan awalnya roadmapnya horizontal, tapi saya buat di mobile vertikal agar muat. terus untuk yang experience sama skills juga saya buat kolomnya menumpuk kebawah tidak ke samping agar muat juga di mobile.

 3. batasan yang saya alami adalah semua informasi yang saya taruh disini seperti (profile, experience, skills dll) itu saya simpan secara manual di file HTMLnya, kalo ada informasi baru saya harus ubah filenya dan deploy ulang. dan juga batasannya adalah pengguna atau user dari web portofolio saya ini masih belum bisa memberi input secara langsung.
 jadi, pada projek selanjutnya fitur dinamis yang mau saya tambahin adalah mengupdate informasi tanpa saya harus ubah file HTMLnya semua karena jadi ribet, lalu fitur agar pengguna bisa masukin input jadi pengguna
 nya bisa mengirim pesan ke saya langsung atau email langsung gitu.

 **AI disclosure**: pada tugas ini saya menggunakan gemini dan claude untuk membantu saya dalam proses saat saya mengalami error, dan buat referensi struktur HTML, dan membantu saya cara menampilkan website pada tampilan mobilenya itu rapih dan tidak sempit. dan saya juga menggunakan ai untuk cek kode CSS saya.


 ### Tugas 2
 1. alur yang terjadi saat pengguna membuka halaman portofolio adalah browser mengirimkan request ke URL yang dituju. Request tersebut pertama kali diterima adalah oleh portofolio/urls.py, lalu dilanjutkan ke main/urls.py. Setelah URL yang sesuai ditemukan, Django menjalankan function view pada main/views.py. View ini ngambil data dari model jika diperlukan (contohnya adalah experience atau skills).kemudian contextnay dikirimkan ke template HTML melalui fungsi render(). Hasil HTML akhirnya dikirim sebagai response buat dikirim ke browser.

 2. Data sebaiknya disimpan di dalam model karena template hanya berguna untuk menampilkan data, kalau model dia mengatur datanya dan menyimpannya dalam database. Dengan disimpan di model, data dapat ditambah, diubah, atau dihapus tanpa kita harus mengedit file HTML secara langsung.

 3. makemigrations digunakan buat membuat file migration berdasarkan perubahan pada model. sedangkan kalo migrate itu digunakan untuk menerapkan migration tersebut ke dalam database. Contohnya adalah ketika saya buat model Skill di main/models.py, saya perlu menjalankan perintah python manage.py makemigrations untuk buat file migration 0002_skill.py. Setelah itu, saya menjalankan perintah python manage.py migrate agar tabel buat model Skill dibuat didalam database.

 **AI Disclosure**  : pada tugas ini saya menggunakan Claude untuk membantu mengecek struktur implementasi model, view, URL, template, dan pengujian pada aplikasi Django. Saya juga menggunakan Claude dan Chatgpt untuk membantu memahami alur request Django, perbedaan perintah `makemigrations` dan `migrate`


## Tugas 3

1. ModelForm digunakan karena formnya langsung terhubung dengan model yang ada di database. Jadi saya tidak perlu membuat semua input dan validasinya secara manual di HTML. Contohnya pada `ProjectForm`, field seperti title, description, dan project_url sudah mengikuti aturan dari model Project. `{% csrf_token %}` digunakan untuk keamanan form, supaya Django bisa memastikan request POST tersebut benar-benar berasal dari halaman website saya dan bukan dari website lain.

2. JSON lebih banyak digunakan pada aplikasi web modern karena formatnya lebih sederhana, ringan, dan mudah dibaca oleh JavaScript. JSON juga langsung cocok dengan bentuk object pada JavaScript. Sedangkan XML biasanya lebih panjang karena menggunakan banyak tag pembuka dan penutup, sehingga ukuran datanya lebih besar dan prosesnya lebih ribet.

3. Saya menggunakan view `get_projects_json` untuk mengembalikan data project dalam bentuk JSON. Sebelum dikirim, data dari model Project perlu diserialization karena data dari database masih berupa QuerySet atau object Django yang tidak bisa langsung dikirim sebagai response JSON. Dengan `serializers.serialize("json", projects)`, data project diubah menjadi format JSON agar bisa dibaca oleh aplikasi lain atau JavaScript di browser.

**AI Disclosure**: pada tugas ini saya menggunakan ChatGPT untuk membantu memahami penggunaan ModelForm, csrf token, serialization JSON, serta mengecek alur fitur create, update, delete, dan JSON data delivery pada aplikasi Django.

## Tugas 4

**AI Disclosure**: Saya menggunakan ChatGPT untuk insight dan mengecek penerapan autentikasi sama otorisasi Django di tugas ini. Saya memberikan konteks ke AI kayak hak akses pengunjung, pengguna biasa, Editor, dan pemilik portofolio. Diskusi saya sama AI difokuskan pada penggunaan Group dan permission change_project, pemeriksaan akses di view dan template, serta pembatasan field yang dikirim oleh endpoint JSON. ChatGPT juga memberikan contoh potongan kode yang saya sesuaikan dengan struktur proyek yang sudah ada.

**Strategi prompting**: Saya menyampaikan aturan akses dari rubrik, lalu meminta AI mengidentifikasi bagian aplikasi yang perlu diperiksa, terutama pas perbedaan hak Editor dan pemilik serta kemungkinan data pengguna ikut terbuka melalui API.

**Evaluasi dan verifikasi**: Saran AI saya gunakan sebagai referensi dan saya sesuaikan dengan model Project, URL, serta template proyek. Saran tersebut tetap perlu diperiksa pada aplikasi yang berjalan karena AI tidak mengetahui kondisi aktual Group, permission, dan database yang saya gunakan. Pengujian akhir untuk setiap role dilakukan dengan memeriksa akses melalui halaman dan URL aksi secara langsung.



## Tugas 5

1. Debouncing menunda request pencarian sampe pengguna berhenti mengetik selama jeda tertentu. lalu pada fitur pencarian proyek, jedanya 300 ms. Ini mengurangi jumlah request yang dikirim ke server dibandingkan mengirim request setiap kali satu karakter diketik.

2. `fetch()` mengembalikan sebuah Promise. `await` membuat fungsi async menunggu sampai Promise tersebut selesai sebelum melanjutkan ke baris berikutnya, misalnya untuk memeriksa status respons dan membaca JSON. Tanpa `await` atau penanganan Promise lain, kode yang membaca respons bisa berjalan sebelum data tersedia.

3. XSS terjadi ketika teks dari pengguna diperlakukan sebagai HTML atau JavaScript oleh browser. Data dari AJAX berisiko jika dimasukkan ke halaman dengan `innerHTML`. Pada halaman proyek, teks dari JSON ditampilkan menggunakan `textContent`, sedangkan input teks dibersihkan di server dengan `strip_tags` melalui `ModelForm`.

**AI Disclosure**: Saya menggunakan ChatGPT untuk membantu membaca checklist Tugas 5, mengecek implementasi AJAXnya, dan mencari kekurangan pada pencarian, token CSRF, lalu buat sanitasi input. Saya meminta AI menjelaskan perubahan yang diperlukan dan memberi contoh kode yang kemudian saya sesuaikan dengan struktur proyek.

**Strategi prompting**: Saya memberikan checklist tugas dan potongan kode proyek saya yang relevan, lalu meminta AI untuk ngecek daftar JSON, pencarian dengan debounce, izin pengguna, CSRF, toast, dan perlindungan XSS.

**Evaluasi dan verifikasi**: Saya memeriksa kode hasil perubahan dan menjalankan `python manage.py check`. Saya juga mengecek tab Network di browser; request pemuatan proyek terlihat sebagai Fetch dengan status HTTP 200. Hasil dari AI tetap perlu dicocokkan dengan rubrik dan diuji di aplikasi karena AI dapat melewatkan masalah seperti kesalahan indentasi atau field yang belum disanitasi.
