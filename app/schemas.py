from marshmallow import Schema, fields


class DepartmentTypeSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class DepartmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    code = fields.Str()
    top_level = fields.Bool()
    parent_id = fields.Int(allow_none=True)
    department_type_id = fields.Int()
    manager_employee_id = fields.Int(allow_none=True, dump_only=True)
    manager_person_id = fields.Int(allow_none=True, dump_only=True)


class PositionSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)


class PersonSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    personal_email = fields.Str()
    org_email = fields.Str(allow_none=True)
    username = fields.Str(allow_none=True)
    id_number = fields.Str()
    tax_id = fields.Str()
    gender = fields.Str(allow_none=True)
    birthdate = fields.Date(allow_none=True)


class PersonDataSchema(Schema):
    id = fields.Int()
    username = fields.Str(allow_none=True)
    first_name = fields.Str()
    last_name = fields.Str()
    personal_email = fields.Str()
    org_email = fields.Str(allow_none=True)
    id_number = fields.Str()
    tax_id = fields.Str()
    gender = fields.Str(allow_none=True)
    birthdate = fields.Date(allow_none=True)
    relationship_type = fields.Str(allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)
    start_date = fields.Date(allow_none=True)
    end_date = fields.Date(allow_none=True)
    status = fields.Str(allow_none=True)
    position = fields.Int(allow_none=True)
    position_name = fields.Str(allow_none=True)
    department_name = fields.Str(allow_none=True)
    department_relation = fields.Str(allow_none=True)
    company_name = fields.Str(allow_none=True)


class DepartmentDataSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    code = fields.Str()
    top_level = fields.Bool()
    parent = fields.Int(allow_none=True)
    parent_name = fields.Str(allow_none=True)
    department_type = fields.Int()
    department_type_name = fields.Str()
    manager_employee_id = fields.Int(allow_none=True)
    manager_person_id = fields.Int(allow_none=True)
    manager_first_name = fields.Str(allow_none=True)
    manager_last_name = fields.Str(allow_none=True)


class EmployeeSchema(Schema):
    id = fields.Int()
    person = fields.Int()
    start_date = fields.Date()
    end_date = fields.Date(allow_none=True)
    position_id = fields.Int(allow_none=True)
    department_id = fields.Int()
    department_relation = fields.Str()


class ContractorSchema(Schema):
    id = fields.Int()
    person = fields.Int()
    start_date = fields.Date()
    end_date = fields.Date(allow_none=True)
    company_name = fields.Str(allow_none=True)
    department_id = fields.Int(allow_none=True)
