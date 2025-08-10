<?php
session_start();

if (isset($_POST['id_produit'])) {
    $id_produit = $_POST['id_produit'];

    foreach ($_SESSION['panier'] as $key => $item) {
        if ($item['id'] == $id_produit) {
            unset($_SESSION['panier'][$key]);
            break;
        }
    }
}

header('Location: panier.php');
exit;
?>
