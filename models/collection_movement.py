
from odoo import models, fields, api
from datetime import datetime, timedelta


class CollectionMovement(models.Model):
    _name = 'collection.movement'
    _description = 'Movimento di Materiale'

    # Riferimento al tipo di materiale
    material_type_id = fields.Many2one(
        'material.type',
        string="Tipo di Materiale",
        required=True
    )

    # Riferimento al punto di raccolta
    collection_point_id = fields.Many2one(
        'collection.point',
        string="Punto di Raccolta",
        required=True
    )

    quantity = fields.Float(string="Quantità", required=True, default=0.0)

    date = fields.Datetime(string="Data Movimento", default=lambda self: fields.Datetime.now())

    status = fields.Selection([
        ('in_attesa', 'In attesa'),
        ('smaltito', 'Smaltito'),
        ('consegnato', 'Consegnato a terzi'),
    ], string="Stato", default='in_attesa', required=True)

    # Campo data scadenza, ad es. per gestire reminder
    deadline_date = fields.Date(string="Data Scadenza Smaltimento")

    # Esempio di metodo per passare da uno stato all'altro
    def action_mark_smaltito(self):
        self.status = 'smaltito'

    def action_mark_consegnato(self):
        self.status = 'consegnato'

    def action_mark_attesa(self):
        self.status = 'in_attesa'

    @api.model
    def cron_send_reminder_for_deadlines(self):
        """
        Metodo chiamato da un cron job per inviare notifiche
        se ci sono movimenti in attesa oltre la loro deadline.
        """
        today = fields.Date.today()
        # Trovo i movimenti scaduti e ancora "in attesa"
        expired_movements = self.search([
            ('status', '=', 'in_attesa'),
            ('deadline_date', '<', today),
            ('deadline_date', '!=', False),
        ])
        if expired_movements:
            # Invia una mail di notifica all'utente manager
            # (in un caso reale potresti cercare un gruppo specifico)
            # Qui come esempio usiamo un broadcast interno in bacheca:
            message_body = f"Sono presenti {len(expired_movements)} movimenti in attesa oltre la deadline."
            self.env['mail.message'].create({
                'body': message_body,
                'subject': "Reminder scadenze smaltimento",
                'model': 'collection.movement',
                'res_id': 0,
                'message_type': 'notification',
                'subtype_id': self.env.ref('mail.mt_comment').id,
            })
