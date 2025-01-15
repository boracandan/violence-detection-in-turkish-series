# Türk Televizyon Dizilerinde Kadına Yönelik Şiddet Tespiti İçin Transkripsiyon Tabanlı Bir Program

## AssemblyAI kullanılarak transkripsiyon ve OpenAI GPT-4o ile analiz süreçleri için Python'da yazılmış tam işlevsel bir kadına yönelik şiddet tespiti projesi.

Bu README hem İngilizce hem de Türkçe olarak mevcuttur:

- [İngilizce Versiyon](README.md)
- [Türkçe Versiyon](README.tr.md)

Bu proje, kadına yönelik şiddetin Türk toplumu ve kültürü üzerindeki etkisini kapsamlı bir şekilde ele alan TÜBİTAK 2204-A araştırma projesi kapsamında geliştirilmiştir. Proje tamamen Python dilinde yazılmıştır ve süreç şu adımları takip etmektedir:

1. **YouTube'dan Veri Toplama**: Televizyon dizilerinin en yüksek izlenme/etkileşim noktalarının saniyeleri YouTube'dan veri kazıma yöntemiyle belirlendi.
2. **Ses Kliplerinin Çıkartılması**: Bu noktalardan en yüksek tekrar izlenme oranına sahip olan %15'lik kısım seçildi ve bu bölümlerden 90 saniyelik ses klipleri (zirve noktasından 45 saniye önce ve sonra) çıkartıldı.
3. **AssemblyAI ile Transkripsiyon**: İndirilen ses klipleri, modern konuşma işleme endüstrisinde lider bir yapay zeka olan AssemblyAI’nin konuşmacı ayrıştırma yöntemi kullanılarak metne dönüştürüldü. AssemblyAI, performans testlerinde diğer modellerden daha doğru sonuçlar verdiği bilinen bir yapıdır (Bkz: [AssemblyAI Benchmark](https://assemblyaiassets.com/pdf/2024%20Speech%20AI%20Benchmarks.pdf)).
4. **OpenAI GPT-4o ile Analiz**: Elde edilen transkriptler, gelişmiş akıl yürütme ve anlama yetenekleriyle bilinen OpenAI’nın GPT-4o modeline verildi (Bkz: [OpenAI GPT-4o Documentation](https://platform.openai.com/docs/models/gpt-4o)). Model, özel istemler temel alınarak, verilen transkriptlerde herhangi bir şekilde kadına yönelik şiddetin (psikolojik, fiziksel, ekonomik vb.) var olup olmadığını tespit etmekle görevlendirildi.
5. **Şiddet Analizi**: Son olarak, dizinin en popüler sahnelerindeki kadına yönelik şiddet oranı analiz sonuçlarına dayanarak hesaplandı ve bölümlerin en çok izlenen bölümlerindeki şiddet içeriği oranı belirlendi.

## Proje Yapısı

Programın tüm mantığı `src` paketinde bulunmaktadır ve `main.py` dosyasında bir örnek kullanım gösterimi sağlanmıştır. Ek olarak, `accuracy_testing` dizini, bu göreve özel olarak OpenAI GPT-4o’nun doğruluk oranını nasıl test ettiğimizi göstermektedir.

## Gereksinimler

Projenin çalışabilmesi için aşağıdaki bağımlılıkların kurulması gereklidir:

- Transkripsiyon için `AssemblyAI`
- GPT-4o analizi için `OpenAI`
- YouTube videolarını indirmek için `yt-dlp`
- Ses işleme için `ffmpeg`
- Diğer bağımlılıklar `requirements.txt` dosyasında listelenmiştir.

### Not:
- **FFmpeg**, kullanıcı tarafından manuel olarak kurulmalıdır. FFmpeg’i [FFmpeg Resmi Sitesi](https://ffmpeg.org/download.html) üzerinden indirebilir ve platformunuza uygun kurulum talimatlarını takip edebilirsiniz.

Gerekli paketleri şu komutla yükleyebilirsiniz:

```bash
pip install -r requirements.txt
```

## Yapılandırma

Proje, yapı sistemi ve paketleme yapılandırmalarını yönetmek için `pyproject.toml` dosyasını kullanır. Proje ayarlarını özelleştirmek, projeyi paketlemek veya bağımlılıkları yönetmek istiyorsanız bu dosyayı kontrol ettiğinizden emin olun.

## Kullanım

Bu projeyi kullanmak için, işlemi göstermek adına `main.py` dosyasındaki talimatları takip edin. AssemblyAI ve OpenAI için API anahtarlarınızı `.env` dosyasına tanımladığınızdan emin olun (örnek bir `.env.example` dosyası verilmiştir).

---

Projenin işlevselliğini daha da geliştirmek için bir sorun açabilir veya katkıda bulunabilirsiniz.