<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class PredictionController extends Controller
{
    public function showForm()
    {
        return view('predict');
    }

    public function predict(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string',
        ]);

        $title = $validated['title'];

        // Melakukan permintaan ke Flask API
        $response = Http::post('http://localhost:5000/predictsdgs', [
            'title' => $title,
        ]);

        // Mengembalikan respons dari Flask API
        if ($response->successful()) {
            $predicted_labels = $response->json()['predicted_labels'];
            return view('result', [
                'title' => $title,
                'predicted_labels' => $predicted_labels,
            ]);
        } else {
            return view('result', [
                'title' => $title,
                'error' => 'Prediction failed',
                'predicted_labels' => [],
            ]);
        }
    }
}
