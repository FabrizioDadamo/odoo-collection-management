
from odoo import models, fields

class MaterialType(models.Model):
    _name = 'material.type'
    _description = 'Tipologia di Materiale'

    name = fields.Char(string="Tipo di Materiale", required=True)
    description = fields.Text(string="Descrizione")