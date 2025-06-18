from odoo import models, fields, api

class FolderArchive(models.Model):
    _name = 'folder.archive'
    _description = 'مجلد الأرشيف'
    _inherit = ['documents.folder']
    _order = 'sequence, name'

    document_ids = fields.One2many('archive.document', 'folder_id', string='الوثائق')
    document_count = fields.Integer(compute='_compute_document_count')

    def _compute_document_count(self):
        for folder in self:
            folder.document_count = len(folder.document_ids)

class DocumentArchive(models.Model):
    _name = 'document.archive'
    _description = 'وثيقة الأرشيف'
    _inherit = ['documents.document', 'mail.thread']
    _order = 'create_date desc'

    group_ids = fields.Many2many('res.groups', string='المجموعات المسموحة')
    folder_id = fields.Many2one('archive.folder', string='مجلد الأرشيف', required=True)
    reference = fields.Char(string='المرجع')
    archive_date = fields.Datetime(string='تاريخ الأرشفة', default=fields.Datetime.now)