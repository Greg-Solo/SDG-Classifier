<?php

use App\Http\Controllers\PredictionController;
use Illuminate\Support\Facades\Route;

Route::get('/predict', [PredictionController::class, 'showForm']);
Route::post('/predict', [PredictionController::class, 'predict']);
Route::get('/result', function () {
    return view('result');
});
