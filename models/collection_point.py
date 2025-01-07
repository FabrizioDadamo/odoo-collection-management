

from odoo import models, fields, api


class CollectionPoint(models.Model):
    _name = 'collection.point'
    _description = 'Punto di Raccolta'

    name = fields.Char(string="Nome del Punto di Raccolta", required=True)
    location = fields.Char(string="Ubicazione")
    capacity = fields.Float(string="Capacità", help="Capacità massima di materiali gestibili in questo punto.")

    # Esempio di campo calcolato per tenere traccia dello spazio occupato
    occupied_capacity = fields.Float(
        string="Capacità Occupata",
        compute="_compute_occupied_capacity",
        store=True
    )

    # Relazione one2many con i movimenti (solo se vogliamo vederli in form view)
    movement_ids = fields.One2many(
        'collection.movement',
        'collection_point_id',
        string="Movimenti"
    )

    @api.depends('movement_ids.quantity', 'movement_ids.status')
    def _compute_occupied_capacity(self):
        """
        Esempio: sommatoria delle quantity di tutti i movimenti
        NON smaltiti / non consegnati
        """
        for record in self:
            # Prendo i movimenti che non siano in "Smaltito" o "Consegnato a terzi"
            active_movements = record.movement_ids.filtered(
                lambda m: m.status in ['in_attesa']
            )
            record.occupied_capacity = sum(m.quantity for m in active_movements)
