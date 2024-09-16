<?php

namespace App\Imports;

use Illuminate\Support\Collection;
use Maatwebsite\Excel\Concerns\ToCollection;

class TitlesImport implements ToCollection
{
    protected $titles = [];

    public function collection(Collection $rows)
    {
        dd($rows);

        foreach ($rows as $row) 
        {
            // Assuming titles are in the first column
            $this->titles[] = $row[1];
        }
    }

    public function getTitles()
    {
        return $this->titles;
    }
}
