<?php
session_start();
try
{
    // Connection à la base de données avec PDO PostgreSQL
    $wilfride = new PDO('pgsql:host=localhost;dbname=lonely;user=postgres;password=wil');
}
catch(Exception $e)
{
    die('Erreur : ' . $e->getMessage());
}

if (isset($_POST['id'])) {
    $id = $_POST['id'];
    $quantite = isset($_POST['quantite']) ? (int) $_POST['quantite'] : 1;

    // Vérifier si le produit existe
    $stmt = $wilfride->prepare("SELECT * FROM produits WHERE id = :id");
    $stmt->execute([':id' => $id]);
    $produit = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($produit) {
        $produit['quantite'] = $quantite;

        if (!isset($_SESSION['panier'])) {
            $_SESSION['panier'] = [];
        }

        // Vérifier si le produit est déjà dans le panier
        $found = false;
        foreach ($_SESSION['panier'] as &$item) {
            if ($item['id'] == $id) {
                $item['quantite'] += $quantite;
                $found = true;
                break;
            }
        }

        if (!$found) {
            $_SESSION['panier'][] = $produit;
        }

        // Enregistrer le traitement dans une variable ou un tableau panier
        $panier = $_SESSION['panier'];
    }
} else {
    echo "Aucun produit sélectionné";
    exit;
}

header('Location: panier.php');
exit;
?>
