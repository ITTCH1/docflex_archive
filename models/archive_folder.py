from odoo import models, fields, api

class ArchiveFolder(models.Model):
    _name = 'archive.folder'
    _description = 'مجلدات الأرشيف'
    _parent_name = "parent_id"
    _parent_store = True
    _order = 'sequence, complete_name'

    name = fields.Char(required=True, string='اسم المجلد')
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one('archive.folder', string='المجلد الأب', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('archive.folder', 'parent_id', string='المجلدات الفرعية')
    sequence = fields.Integer(default=10)
    complete_name = fields.Char('المسار الكامل', compute='_compute_complete_name', store=True)
    description = fields.Text('الوصف')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    document_ids = fields.One2many('archive.document', 'folder_id', string='الوثائق')
    document_count = fields.Integer(compute='_compute_document_count')
    color = fields.Integer('لون المؤشر')
    barcode = fields.Char('الباركود', copy=False)
    type = fields.Selection([
        ('physical', 'أرشيف ورقى'),
        ('digital', 'أرشيف إلكتروني'),
        ('mixed', 'مختلط')
    ], string='نوع الأرشيف', default='physical')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for folder in self:
            if folder.parent_id:
                folder.complete_name = f"{folder.parent_id.complete_name}/{folder.name}"
            else:
                folder.complete_name = folder.name

    def _compute_document_count(self):
        for folder in self:
            folder.document_count = len(folder.document_ids)

    @api.model
    def create(self, vals):
        if not vals.get('barcode'):
            vals['barcode'] = self.env['ir.sequence'].next_by_code('archive.folder.barcode')
        return super().create(vals)

    def name_get(self):
        return [(folder.id, folder.complete_name) for folder in self]

    def action_open_documents(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'وثائق {self.name}',
            'res_model': 'archive.document',
            'view_mode': 'tree,form',
            'domain': [('folder_id', '=', self.id)],
            'context': {
                'default_folder_id': self.id,
                'create': False
            },
        }