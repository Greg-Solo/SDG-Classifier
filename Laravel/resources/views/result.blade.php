<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">

    <title>Scholar - Online School HTML5 Template</title>

    <!-- Bootstrap core CSS -->
    <link href="../vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">


    <!-- Additional CSS Files -->
    <link rel="stylesheet" href="../assets/css/fontawesome.css">
    <link rel="stylesheet" href="../assets/css/template.css">
    <link rel="stylesheet" href="../assets/css/owl.css">
    <link rel="stylesheet" href="../assets/css/animate.css">
    <link rel="stylesheet"href="https://unpkg.com/swiper@7/swiper-bundle.min.css"/>
    <style>
      .header-text h1, h2, h3 {
          color: white; /* Ganti dengan warna yang Anda inginkan */
          font-weight: bold; /* Menambahkan gaya huruf tebal */
      }
      /* h2, h3 {
        color: #090909;
      } */
      .label-container {
          padding: 10px;
          background-color: #f9f9f9;
          border: 1px solid #ddd;
          border-radius: 5px;
          margin-bottom: 10px;
      }
  </style>
  </head>

<body class="presentation-page bg-gray-200">

  <!-- ***** Preloader Start ***** -->
  <div id="js-preloader" class="js-preloader">
    <div class="preloader-inner">
      <span class="dot"></span>
      <div class="dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  </div>
  <!-- ***** Preloader End ***** -->

  <!-- ***** Header Area Start ***** -->
  <header class="header-area header-sticky">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <nav class="main-nav">
                    <!-- ***** Logo Start ***** -->
                    <a href="index.html" class="logo">
                        <h1>SDGS</h1>
                    </a>
                    <!-- ***** Logo End ***** -->
            
                    <!-- ***** Menu Start ***** -->
                    <ul class="nav">
                      <li class="scroll-to-section"><a href="../index.html" class="active">Back to Home</a></li>
                  </ul>   
                    <a class='menu-trigger'>
                        <span>Menu</span>
                    </a>
                    <!-- ***** Menu End ***** -->
                </nav>
            </div>
        </div>
    </div>
  </header>
  <!-- ***** Header Area End ***** -->

  <div class="main-banner" id="top">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <div class="owl-carousel owl-banner">
                        <div class="item item-1">
                            <div class="header-text">
                                <h2>Hasil Prediksi judul</h2>
                                
                                @foreach ($predictions as $prediction)
                                    <h3>Judul: {{ $prediction['title'] }}</h3> <!-- New line: Display each title -->
                                    @if (isset($prediction['predicted_labels']) && count($prediction['predicted_labels']) > 0) <!-- New line: Check if labels exist -->
                                        <p>Label SDG:</p>
                                        <div class="label-list">
                                            @foreach ($prediction['predicted_labels'] as $label) <!-- New line: Loop through labels -->
                                                <div class="label-container">
                                                    <li>{{ $label }}</li>
                                                </div>
                                            @endforeach
                                        </div>
                                    @else
                                        <p>{{ $prediction['error'] ?? 'Prediction failed' }}</p> <!-- New line: Display error if prediction failed -->
                                    @endif
                                @endforeach <!-- New line: End loop -->
                                <a href="{{ url('/predict') }}" class="btn btn-primary">Predict Again</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


  <footer>
    <div class="container">
      <div class="col-lg-12">
        <p>Direktorat Sistem Informasi Universitas Airlangga</a></p>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <!-- Bootstrap core JavaScript -->
  <script src="../vendor/jquery/jquery.min.js"></script>
  <script src="../vendor/bootstrap/js/bootstrap.min.js"></script>
  <script src="../assets/js/isotope.min.js"></script>
  <script src="../assets/js/owl-carousel.js"></script>
  <script src="../assets/js/counter.js"></script>
  <script src="../assets/js/custom.js"></script>

  </body>
</html>