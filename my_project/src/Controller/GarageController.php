<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class AirExplorerController extends AbstractController
{
    #[Route('/air/explorer', name: 'app_air_explorer')]
    public function index(): Response
    {
        return $this->render('air_explorer/index.html.twig', [
            'controller_name' => 'AirExplorerController',
        ]);
    }
}
