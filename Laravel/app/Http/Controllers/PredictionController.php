<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Maatwebsite\Excel\Facades\Excel;
use App\Imports\TitlesImport;

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
            
        // $validated = $request->validate([
        //     'titles' => 'nullable|string',
        //     'file' => 'nullable|file|mimes:xlsx,csv',
        // ]);
        
        $titlesInput = $request->input('titles');
        // $titlesInput = $validated['titles'];
        $titles =[];
        $idntitles = [];

        // dd($request);
        // dd($titlesInput);

        // if($request->has('titles') && !empty($titles)){
        if($titlesInput){
            // $titlesInput = $request->input('titles');
            
            // dd($request);

            $titles = preg_split('/\r\n|\r|\n/', $titlesInput[0]);
            // dd($titles);
        }
        
        if($request->hasFile('file')){
            // dd($request);
            $file = $request->file('file');
            // dd($file);
            // $import = new TitlesImport;
            // Excel::import($import, $file);
            // $titles = array_merge($titles, $import->getTitles());

            // $titlesFromFile = Excel::toCollection(new TitlesImport, $file);
            $collection = Excel::toCollection(null, $file);
            // $idFromFile = $collection->first()->skip(1)->pluck(0)->toArray();
            // $titlesFromFile = $collection->first()->skip(1)->pluck(1)->toArray();
            $titlesFromFile = $collection->first()->skip(1)->map(function ($row) {
                return [
                    'id' => $row[0], // id col
                    'title' => $row[1], // judul col
                ];
            })->toArray();

            // $titles = array_merge($titles, $titlesFromFile->flatten()->toArray());
            $titles = array_merge($titles, $titlesFromFile);
        }
        
        // dd($titles);

        // $predictions = [];
        $individualPredictions = [];


        // Melakukan permintaan ke Flask API
        foreach($titles as $entry){ // $title == entry
            $id = $entry['id'];
            $title = $entry['title'];

            if(!empty($title)){
                $response = Http::post('http://localhost:5000/predictsdgs', [
                    'title' => $title,
                ]);
    
                // Mengembalikan respons dari Flask API
                if ($response->successful()) {
                    $predicted_labels = $response->json()['predicted_labels'];
                    // $predictions[] = [
                    //     'title' => $title,
                    //     'predicted_labels' => $predicted_labels,
                    // ];

                    foreach($predicted_labels as $label){
                        $individualPredictions[] = [
                            'id' => $id,
                            'title' => $title,
                            'predicted_label' => $label,
                        ];
                    }
                } else {
                    // $predictions[] = [
                    //     'title' => $title,
                    //     'error' => 'Prediction Failed',
                    //     'predicted_labels' => [],
                    // ];

                    $individualPredictions[] = [
                        'id' => $id,
                        'title' => $title,
                        'error' => 'Prediction Failed',
                        'predicted_label' => null,
                    ];
                }
            }
        }

        return view('result', [
            // 'predictions' => $predictions,
            'predictions' => $individualPredictions,
        ]);
    }
}
