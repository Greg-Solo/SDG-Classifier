# SDG Classifier for Journals
This is the source code for a website that hosts an SDG Classifier Model. This project was build using [Laravel](#about-laravel).

**Input**:
- Journal title(s)
- Excel or csv file containing journal titles

**Output**:
- One or more SDGs related to each titles.

<br/>

## Requirements
Below are the requirements to run this project locally.

> **_<font style="color: blue;">NOTE</font>_**  
> All Python packages can be installed using the `requirements.txt` file. More in [3. Setup Steps](#setup)

**PHP**
- PHP (8.2.22)
- Composer (2.7.8)
- Laravel Framework (11.21.0)

**PHP Packages**
- maatwebsite/excel (^3.1)

**Python**
<!-- - Python (3.10)
- Tensorflow (2.17)
- NLTK (3.9.1) -->

- Flask (3.0.3)
- joblib (1.4.2)
- keras (3.5.0)
- nltk (3.9.1)
- numpy (1.26.4)
- pandas (2.2.2)
- regex (2024.7.24)
- scikit-learn (1.5.1)
- tensorflow (2.17.0)

> **_<font style="color: red;">WARNING</font>_**  
> **Avoid using Anaconda** in setting up the environment and installing packages. To avoid problems, **install packages using pip**, and use python's `venv` (optional).

> **_<font style="color: blue;">NOTE</font>_**  
> All of the required PHP packages are already listed in `composer.lock`. Versions of packages unspecified here should automatically be adjusted during installation.

<br/>

## SETUP
Here are the steps to run the project locally.

### 1. Clone The Repo
Clone the entire repository. Make sure all the files are cloned successfully, including the model file (`model.h5`).

### 2. Setup PHP Environment
For more detailed instructions, especially to set up the Laravel environment, see [this Laravel documentation](https://laravel.com/docs/11.x#creating-a-laravel-project).

> **_<font style="color: blue;">NOTE</font>_**  
> It is recommended to install **Laravel installer** globally as mentioned in the documentation.

1. **Install PHP**  
   - [**Official** Installation & Configuration](https://www.php.net/manual/en/install.php)
   - [Installing on Ubuntu](https://www.cherryservers.com/blog/how-to-install-php-ubuntu)

2. **Install Composer**  
   See [Composer documentation](https://getcomposer.org/doc/00-intro.md).

3. **Install Laravel**  
   See [Laravel documentation](https://laravel.com/docs/11.x/installation).

4. **Set Up The PHP environment**  
   `cd` to the `Laravel` directory and run `composer install` to install necessary PHP packages.


### 3. **Set Up The Python Environment**
   1. **Create a virtual environment (optional)**  
      ```
      python -m venv <env_name>
      ```
      The directory of the virtual environment is usually created in `~/.virtualenvs` or in the directory where you run the command.

      To activate the virtual environment, run:
      ```
      source <venv_dir_name>/bin/activate
      ```

   2. **Install neccesary python libraries**  
      There should be a `requirements.txt` file in the root directory of the proc. Run this command from the root directory to install all python requirements.
      ```
      pip install -r ./requirements.txt
      ```
      Make sure that the correct version of packages listed in [2. Requirements](#requirements) are installed.

### 4. **Run the project**
   1. `cd` to `Laravel` directory and run:
      ```
      php artisan serve
      ```
   2. In another terminal, stay on the root directory and run:
      ```
      python app.py
      ```

> **_<font style="color: blue;">NOTE</font>_**  
> If you're using a virtual environment, make sure that it's active before running `app.py`

<br/>

## More Info
This project was build using **Laravel**.

<p align="center">
    <a href="https://laravel.com" target="_blank">
        <img src="https://raw.githubusercontent.com/laravel/art/master/logo-lockup/5%20SVG/2%20CMYK/1%20Full%20Color/laravel-logolockup-cmyk-red.svg" width="400" alt="Laravel Logo">
    </a>
</p>

<p align="center">
    <a href="https://github.com/laravel/framework/actions">
        <img src="https://github.com/laravel/framework/workflows/tests/badge.svg" alt="Build Status">
    </a>
    <a href="https://packagist.org/packages/laravel/framework">
        <img src="https://img.shields.io/packagist/dt/laravel/framework" alt="Total Downloads">
    </a>
    <a href="https://packagist.org/packages/laravel/framework">
        <img src="https://img.shields.io/packagist/v/laravel/framework" alt="Latest Stable Version">
    </a>
    <a href="https://packagist.org/packages/laravel/framework">
        <img src="https://img.shields.io/packagist/l/laravel/framework" alt="License">
    </a>
</p>

## About Laravel

Laravel is a web application framework with expressive, elegant syntax. We believe development must be an enjoyable and creative experience to be truly fulfilling. Laravel takes the pain out of development by easing common tasks used in many web projects, such as:

- [Simple, fast routing engine](https://laravel.com/docs/routing).
- [Powerful dependency injection container](https://laravel.com/docs/container).
- Multiple back-ends for [session](https://laravel.com/docs/session) and [cache](https://laravel.com/docs/cache) storage.
- Expressive, intuitive [database ORM](https://laravel.com/docs/eloquent).
- Database agnostic [schema migrations](https://laravel.com/docs/migrations).
- [Robust background job processing](https://laravel.com/docs/queues).
- [Real-time event broadcasting](https://laravel.com/docs/broadcasting).

Laravel is accessible, powerful, and provides tools required for large, robust applications.

## Learning Laravel

Laravel has the most extensive and thorough [documentation](https://laravel.com/docs) and video tutorial library of all modern web application frameworks, making it a breeze to get started with the framework.

You may also try the [Laravel Bootcamp](https://bootcamp.laravel.com), where you will be guided through building a modern Laravel application from scratch.

If you don't feel like reading, [Laracasts](https://laracasts.com) can help. Laracasts contains thousands of video tutorials on a range of topics including Laravel, modern PHP, unit testing, and JavaScript. Boost your skills by digging into our comprehensive video library.

## Laravel Sponsors

We would like to extend our thanks to the following sponsors for funding Laravel development. If you are interested in becoming a sponsor, please visit the [Laravel Partners program](https://partners.laravel.com).

### Premium Partners

- **[Vehikl](https://vehikl.com/)**
- **[Tighten Co.](https://tighten.co)**
- **[WebReinvent](https://webreinvent.com/)**
- **[Kirschbaum Development Group](https://kirschbaumdevelopment.com)**
- **[64 Robots](https://64robots.com)**
- **[Curotec](https://www.curotec.com/services/technologies/laravel/)**
- **[Cyber-Duck](https://cyber-duck.co.uk)**
- **[DevSquad](https://devsquad.com/hire-laravel-developers)**
- **[Jump24](https://jump24.co.uk)**
- **[Redberry](https://redberry.international/laravel/)**
- **[Active Logic](https://activelogic.com)**
- **[byte5](https://byte5.de)**
- **[OP.GG](https://op.gg)**

## Contributing

Thank you for considering contributing to the Laravel framework! The contribution guide can be found in the [Laravel documentation](https://laravel.com/docs/contributions).

## Code of Conduct

In order to ensure that the Laravel community is welcoming to all, please review and abide by the [Code of Conduct](https://laravel.com/docs/contributions#code-of-conduct).

## Security Vulnerabilities

If you discover a security vulnerability within Laravel, please send an e-mail to Taylor Otwell via [taylor@laravel.com](mailto:taylor@laravel.com). All security vulnerabilities will be promptly addressed.

## License

The Laravel framework is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
