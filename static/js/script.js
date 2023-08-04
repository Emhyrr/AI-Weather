// Menangkap elemen input file
const fileInput = document.getElementById('file-upload');

// Menangkap elemen img-area
const imgArea = document.querySelector('.img-area');

// Menambahkan event listener ketika terjadi perubahan pada input file
fileInput.addEventListener('change', function() {
  // Mengambil file yang diunggah
  const file = fileInput.files[0];

  // Membaca file sebagai URL gambar
  const reader = new FileReader();

  reader.onload = function(e) {
    // Mengatur atribut data-img pada img-area dengan URL gambar
    imgArea.setAttribute('data-img', e.target.result);
    // Menampilkan gambar di img-area
    imgArea.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;
  }

  reader.readAsDataURL(file);
});


