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
        // $validated = $request->validate([
        //     'titles' => 'required|string',
        //     // 'titles' => 'required|array',
        //     // 'titles.*' => 'required|string',
        // ]);

        $titlesInput = $request->input('titles');
        
        // $titles = $validated['titles'];
        // $titles = preg_split('/\r\n|\r|\n/', $validated['titles']);
        $titles = preg_split('/\r\n|\r|\n/', $titlesInput[0]);
        // dd($titles);
        

        $predictions = [];


        // Melakukan permintaan ke Flask API
        foreach($titles as $title){
            if(!empty($title)){
                $response = Http::post('http://localhost:5000/predictsdgs', [
                    'title' => $title,
                ]);
    
                // Mengembalikan respons dari Flask API
                if ($response->successful()) {
                    $predicted_labels = $response->json()['predicted_labels'];
                    $predictions[] = [
                        'title' => $title,
                        'predicted_labels' => $predicted_labels,
                    ];
                } else {
                    $predictions[] = [
                        'title' => $title,
                        'error' => 'Prediction Failed',
                        'predicted_labels' => [],
                    ];
                }
            }
        }

        return view('result', [
            'predictions' => $predictions,
        ]);

    }
}
