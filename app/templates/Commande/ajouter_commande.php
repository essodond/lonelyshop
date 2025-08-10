<?php
require_once('Commande.class.php');

try {
    $db = new PDO('pgsql:host=localhost;dbname=lonely;user=postgres;password=wil');
    $commande = new Commande($db);
    
    if (!isset($_POST['utilisateur_id']) || !isset($_POST['total']) || 
        !isset($_POST['statut']) || !isset($_POST['date_commande'])) {
        die('Missing required fields');
    }

    $commande->setUtilisateurId($_POST['utilisateur_id']);
    $commande->setTotal($_POST['total']);
    $commande->setStatut($_POST['statut']);
    $commande->setDateCommande($_POST['date_commande']);

    if ($commande->createCommande()) {
        echo "Commande ajoutée avec succès.";
    } else {
        echo "Erreur lors de l'ajout de la commande.";
    }
} catch(Exception $e) {
    die('Erreur : ' . $e->getMessage());
}
?>
// Retrieve the product ID from the POST request
$produit_id = $_POST['produit_id'];
<?php
session_start();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Nouvelle Commande</title>
</head>
<body>
    <h2>Ajouter une nouvelle commande</h2>
    <form action="ajouter_commande.php" method="POST">
        <input type="hidden" name="utilisateur_id" value="<?php echo isset($_SESSION['user_id']) ? $_SESSION['user_id'] : ''; ?>">
        
        <div>
            <label for="total">Total:</label>
            <input type="number" name="total" step="0.01" required>
        </div>

        <div>
            <label for="statut">Statut:</label>
            <select name="statut" required>
                <option value="en_attente">En attente</option>
                <option value="confirmee">Confirmée</option>
                <option value="expediee">Expédiée</option>
            </select>
        </div>

        <div>
            <label for="date_commande">Date de commande:</label>
            <input type="date" name="date_commande" value="<?php echo date('Y-m-d'); ?>" required>
        </div>

        <button type="submit">Ajouter la commande</button>
    </form>
</body>
</html>
