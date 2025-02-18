<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class CarInfoController extends AbstractController
{
    /**
     * @Route("/car/{id}", name="car_info")
     */
    public function index(int $id): Response
    {
        // Fetch car information based on the ID
        $car = $this->getCarInfoById($id);

        return $this->render('car_info/index.html.twig', [
            'car' => $car,
        ]);
    }

    private function getCarInfoById(int $id)
    {
        // Dummy data for demonstration purposes
        $cars = [
            1 => ['name' => 'Car 1', 'details' => 'Details about Car 1'],
            2 => ['name' => 'Car 2', 'details' => 'Details about Car 2'],
            // Add more cars as needed
        ];

        return $cars[$id] ?? null;
    }
}
