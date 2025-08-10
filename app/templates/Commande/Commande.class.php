<?php
class Commande {
    private $db;
    private $table = "commandes";

    // Properties
    private $id;
    private $utilisateur_id;
    private $total;
    private $statut;
    private $date_commande;

    // Constructor
    public function __construct($database) {
        $this->db = $database;
    }

    // Setters
    public function setUtilisateurId($utilisateur_id) {
        $this->utilisateur_id = $utilisateur_id;
    }

    public function setTotal($total) {
        $this->total = $total;
    }

    public function setStatut($statut) {
        $this->statut = $statut;
    }

    public function setDateCommande($date_commande) {
        $this->date_commande = $date_commande;
    }

    // Create new order
    public function createCommande() {
        try {
            $query = "INSERT INTO " . $this->table . " 
                    (utilisateur_id, total, statut, date_commande) 
                    VALUES 
                    (:utilisateur_id, :total, :statut, :date_commande)";

            $stmt = $this->db->prepare($query);

            $stmt->bindParam(':utilisateur_id', $this->utilisateur_id, PDO::PARAM_INT);
            $stmt->bindParam(':total', $this->total, PDO::PARAM_STR);
            $stmt->bindParam(':statut', $this->statut, PDO::PARAM_STR);
            $stmt->bindParam(':date_commande', $this->date_commande, PDO::PARAM_STR);

            return $stmt->execute();
        } catch(PDOException $e) {
            error_log("Error creating order: " . $e->getMessage());
            return false;
        }
    }

    // Get orders by user ID
    public function getCommandesByUser($utilisateur_id) {
        try {
            $query = "SELECT * FROM " . $this->table . " 
                    WHERE utilisateur_id = :utilisateur_id 
                    ORDER BY date_commande DESC";
                    
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':utilisateur_id', $utilisateur_id, PDO::PARAM_INT);
            $stmt->execute();
            
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch(PDOException $e) {
            error_log("Error fetching orders: " . $e->getMessage());
            return false;
        }
    }

    // Get single order by ID
    public function getCommandeById($id) {
        try {
            $query = "SELECT * FROM " . $this->table . " WHERE id = :id";
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':id', $id, PDO::PARAM_INT);
            $stmt->execute();
            
            return $stmt->fetch(PDO::FETCH_ASSOC);
        } catch(PDOException $e) {
            error_log("Error fetching order: " . $e->getMessage());
            return false;
        }
    }

    // Update order status
    public function updateStatut($id, $statut) {
        try {
            $query = "UPDATE " . $this->table . " 
                    SET statut = :statut 
                    WHERE id = :id";
                    
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':id', $id, PDO::PARAM_INT);
            $stmt->bindParam(':statut', $statut, PDO::PARAM_STR);
            
            return $stmt->execute();
        } catch(PDOException $e) {
            error_log("Error updating order status: " . $e->getMessage());
            return false;
        }
    }
}
?>