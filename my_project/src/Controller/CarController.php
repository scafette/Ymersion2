<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
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
    public function index(Request $request): Response
    {
        $id = $request->query->get('page');
    
        if ($id) {    
            if ($id == 1) {
                $apiUrl = "http://127.0.0.1:5000/first30";
            } else if ($id == 2) {
                $apiUrl = "http://127.0.0.1:5000/cars/last33";
            }
        } else {
            $apiUrl = "http://127.0.0.1:5000/cars/first30";
        }

        $response = $this->client->request('GET', $apiUrl);
        $cars = $response->toArray();

        return $this->render('cars/cars.html.twig', [
            'cars' => $cars
        ]);
    }

    #[Route('/cars/{id}', name: 'app_car', methods: ['GET'])]
    public function show(int $id): Response
    {
        $apiUrl = "http://127.0.0.1:5000/cars/" . $id;

        $response = $this->client->request('GET', $apiUrl);
        
        if ($response->getStatusCode() !== 200) {
            throw $this->createNotFoundException("Voiture non trouvée");
        }

        $car = $response->toArray();

        return $this->render('cars/car_details.html.twig', [
            'car' => $car
        ]);
    }
    
    #[Route('/cars/{id}/like', name: 'like_car', methods: ['POST'])]
public function likeCar(int $id, Request $request, \Doctrine\DBAL\Connection $connection): Response
{
    $userId = $this->getUser()->getId(); // Vérifie que l'utilisateur est connecté

    // Vérifier si l'utilisateur a déjà liké la voiture
    $existingLike = $connection->fetchOne("SELECT id FROM likes WHERE car_id = ? AND user_id = ?", [$id, $userId]);

    if ($existingLike) {
        // Supprimer le like (toggle)
        $connection->executeQuery("DELETE FROM likes WHERE car_id = ? AND user_id = ?", [$id, $userId]);
        $liked = false;
    } else {
        // Ajouter un like
        $connection->executeQuery("INSERT INTO likes (car_id, user_id) VALUES (?, ?)", [$id, $userId]);
        $liked = true;
    }

    // Récupérer le nouveau nombre de likes
    $likeCount = $connection->fetchOne("SELECT COUNT(*) FROM likes WHERE car_id = ?", [$id]);

    return $this->json(["liked" => $liked, "likes" => $likeCount]);
}

#[Route('/cars/{id}/likes', name: 'get_car_likes', methods: ['GET'])]
public function getCarLikes(int $id, \Doctrine\DBAL\Connection $connection): Response
{
    $likeCount = $connection->fetchOne("SELECT COUNT(*) FROM likes WHERE car_id = ?", [$id]);

    return $this->json(["likes" => $likeCount]);
}

}
