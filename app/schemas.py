from marshmallow import Schema, fields


class DepartmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)


class PositionSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    department_id = fields.Int(allow_none=True)
    # extra field returned by API
    department_name = fields.Str(allow_none=True)


class PersonSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    personal_email = fields.Str()
    org_email = fields.Str(allow_none=True)
    username = fields.Str(allow_none=True)
    id_number = fields.Str()
    tax_id = fields.Str()
    # workforce view columns
    workforce_id = fields.Int(allow_none=True)
    work_type = fields.Str(allow_none=True)
    manager = fields.Int(allow_none=True)
    start_date = fields.Date(allow_none=True)
    end_date = fields.Date(allow_none=True)


class EmployeeSchema(Schema):
    id = fields.Int()
    person = fields.Int()
    start_date = fields.Date()
    end_date = fields.Date(allow_none=True)
    position_id = fields.Int(allow_none=True)
    manager_id = fields.Int(allow_none=True)


class ContractorSchema(Schema):
    id = fields.Int()
    person = fields.Int()
    start_date = fields.Date()
    end_date = fields.Date(allow_none=True)
    company_name = fields.Str(allow_none=True)
    department_id = fields.Int(allow_none=True)
    manager_id = fields.Int(allow_none=True)
