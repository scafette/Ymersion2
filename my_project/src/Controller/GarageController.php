<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class GarageController extends AbstractController
{
    #[Route('/garage', name: 'app_garage')]
    public function index(): Response
    {
        return $this->render('garage/index.html.twig', [
            'controller_name' => 'GarageController',
        ]);
    }
}
