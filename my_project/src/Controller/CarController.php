<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Contracts\HttpClient\HttpClientInterface;

class CarController extends AbstractController
{
    private $client;

    public function __construct(HttpClientInterface $client)
    {
        $this->client = $client;
    }

    #[Route('/cars', name: 'app_cars')]
    public function index(): Response
    {
        $apiUrl = "http://127.0.0.1:5000/cars";

        $response = $this->client->request('GET', $apiUrl);
        $cars = $response->toArray();

        return $this->render('cars/cata.html.twig', [
            'cars' => $cars
        ]);
    }
}
