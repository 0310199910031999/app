from typing import Optional
import datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, REAL, Sequence, SmallInteger, Boolean, String, Time, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from shared.db import Base



class ClientEquipmentProperty(Base):
    __tablename__ = 'client_equipment_property'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='client_equipment_property_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment: Mapped[Optional[str]] = mapped_column(String(100))
    brand: Mapped[Optional[str]] = mapped_column(String(100))
    model: Mapped[Optional[str]] = mapped_column(String(100))
    serial_number: Mapped[Optional[str]] = mapped_column(String(200))
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    doh: Mapped[Optional[float]] = mapped_column(REAL)

    fopc02: Mapped[list['Fopc02']] = relationship('Fopc02', back_populates='property')
    fopp02: Mapped[list['Fopp02']] = relationship('Fopp02', back_populates='property')


class Clients(Base):
    __tablename__ = 'clients'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='clients_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(200))
    rfc: Mapped[Optional[str]] = mapped_column(String(100))
    address: Mapped[Optional[str]] = mapped_column(String(800))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    contact_person: Mapped[Optional[str]] = mapped_column(String(200))
    email: Mapped[Optional[str]] = mapped_column(String(150))
    status: Mapped[Optional[str]] = mapped_column(String(30))

    app_users: Mapped[list['AppUsers']] = relationship('AppUsers', back_populates='client')
    equipment: Mapped[list['Equipment']] = relationship('Equipment', back_populates='client')
    files: Mapped[list['Files']] = relationship('Files', back_populates='client')
    fobc01: Mapped[list['Fobc01']] = relationship('Fobc01', back_populates='client')
    focr02: Mapped[list['Focr02']] = relationship('Focr02', back_populates='client')
    foem01: Mapped[list['Foem01']] = relationship('Foem01', back_populates='client')
    foem01_1: Mapped[list['Foem011']] = relationship('Foem011', back_populates='client')
    foim01: Mapped[list['Foim01']] = relationship('Foim01', back_populates='client')
    foim03: Mapped[list['Foim03']] = relationship('Foim03', back_populates='client')
    fole01: Mapped[list['Fole01']] = relationship('Fole01', back_populates='client')
    foos01: Mapped[list['Foos01']] = relationship('Foos01', back_populates='client')
    fopc02: Mapped[list['Fopc02']] = relationship('Fopc02', back_populates='client')
    fosc01: Mapped[list['Fosc01']] = relationship('Fosc01', back_populates='client')
    fosp01: Mapped[list['Fosp01']] = relationship('Fosp01', back_populates='client')
    foro05_services: Mapped[list['Foro05Services']] = relationship('Foro05Services', back_populates='client')


class EquipmentBrands(Base):
    __tablename__ = 'equipment_brands'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='equipment_brands_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    img_path: Mapped[Optional[str]] = mapped_column(String(100))

    equipment: Mapped[list['Equipment']] = relationship('Equipment', back_populates='brand')


class EquipmentTypes(Base):
    __tablename__ = 'equipment_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='equipment_types_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))

    equipment: Mapped[list['Equipment']] = relationship('Equipment', back_populates='type')


class FocrAddEquipment(Base):
    __tablename__ = 'focr_add_equipment'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='focr_add_equipment_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment: Mapped[Optional[str]] = mapped_column(String(100))
    brand: Mapped[Optional[str]] = mapped_column(String(100))
    model: Mapped[Optional[str]] = mapped_column(String(100))
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))
    equipment_type: Mapped[Optional[str]] = mapped_column(String(50))
    economic_number: Mapped[Optional[str]] = mapped_column(String(50))
    capability: Mapped[Optional[str]] = mapped_column(String(50))
    addition: Mapped[Optional[str]] = mapped_column(String(100))

    focr02: Mapped[list['Focr02']] = relationship('Focr02', back_populates='additional_equipment')


class FoimQuestions(Base):
    __tablename__ = 'foim_questions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='foim_questions_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    function: Mapped[Optional[str]] = mapped_column(String(250))
    question: Mapped[Optional[str]] = mapped_column(String(250))
    target: Mapped[Optional[str]] = mapped_column(String(50))

    foim01_answers: Mapped[list['Foim01Answers']] = relationship('Foim01Answers', back_populates='foim_question')
    foim03_answers: Mapped[list['Foim03Answers']] = relationship('Foim03Answers', back_populates='foim_question')


class Foir02RequieredEquipment(Base):
    __tablename__ = 'foir02_requiered_equipment'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='foir02_requiered_equipment_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[Optional[int]] = mapped_column(Integer)
    unit: Mapped[Optional[str]] = mapped_column(String(20))
    type: Mapped[Optional[str]] = mapped_column(String(150))
    name: Mapped[Optional[str]] = mapped_column(String(150))

    foir02_equipment_checklist: Mapped[list['Foir02EquipmentChecklist']] = relationship('Foir02EquipmentChecklist', back_populates='equipment')


class FopcServices(Base):
    __tablename__ = 'fopc_services'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='fopc_services_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    foos01: Mapped[list['Foos01']] = relationship('Foos01', back_populates='fopc_services')
    fopc02: Mapped[list['Fopc02']] = relationship('Fopc02', back_populates='fopc_services')
    fosc01: Mapped[list['Fosc01']] = relationship('Fosc01', back_populates='fopc_services')
    fosp01: Mapped[list['Fosp01']] = relationship('Fosp01', back_populates='fopc_services')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='roles_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role_name: Mapped[Optional[str]] = mapped_column(String(30))

    employees: Mapped[list['Employees']] = relationship('Employees', back_populates='role')


class Services(Base):
    __tablename__ = 'services'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='services_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[Optional[str]] = mapped_column(String(50))
    name: Mapped[Optional[str]] = mapped_column(String(150))
    description: Mapped[Optional[str]] = mapped_column(String(600))
    type: Mapped[Optional[str]] = mapped_column(String(50))

    fole01_services: Mapped[list['Fole01Services']] = relationship('Fole01Services', back_populates='service')
    foos01_services: Mapped[list['Foos01Services']] = relationship('Foos01Services', back_populates='service')
    fosc01_services: Mapped[list['Fosc01Services']] = relationship('Fosc01Services', back_populates='service')
    fosp01_services: Mapped[list['Fosp01Services']] = relationship('Fosp01Services', back_populates='service')
    foro05_services: Mapped[list['Foro05Services']] = relationship('Foro05Services', back_populates='service')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)


class Vendors(Base):
    __tablename__ = 'vendors'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='vendors_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    rfc: Mapped[Optional[str]] = mapped_column(String(100))
    contact_person: Mapped[Optional[str]] = mapped_column(String(200))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    address: Mapped[Optional[str]] = mapped_column(String(100))

    fopp02: Mapped[list['Fopp02']] = relationship('Fopp02', back_populates='vendor')


class AppUsers(Base):
    __tablename__ = 'app_users'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='app_users_client_id_fkey'),
        PrimaryKeyConstraint('id', name='app_users_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    lastname: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    password: Mapped[Optional[str]] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    token_fcm: Mapped[Optional[str]] = mapped_column(String(250))

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='app_users')
    foim03: Mapped[list['Foim03']] = relationship('Foim03', back_populates='app_user')


class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['roles.id'], name='employees_role_id_fkey'),
        PrimaryKeyConstraint('id', name='employees_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    lastname: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    password: Mapped[Optional[str]] = mapped_column(String(100))
    session_token: Mapped[Optional[str]] = mapped_column(String(250))

    role: Mapped[Optional['Roles']] = relationship('Roles', back_populates='employees')
    fobc01: Mapped[list['Fobc01']] = relationship('Fobc01', back_populates='employee')
    focr02: Mapped[list['Focr02']] = relationship('Focr02', back_populates='employee')
    foem01: Mapped[list['Foem01']] = relationship('Foem01', back_populates='employee')
    foem01_1: Mapped[list['Foem011']] = relationship('Foem011', back_populates='employee')
    foim01: Mapped[list['Foim01']] = relationship('Foim01', back_populates='employee')
    foim03: Mapped[list['Foim03']] = relationship('Foim03', back_populates='employee')
    fole01: Mapped[list['Fole01']] = relationship('Fole01', back_populates='employee')
    foos01: Mapped[list['Foos01']] = relationship('Foos01', back_populates='employee')
    fopc02: Mapped[list['Fopc02']] = relationship('Fopc02', back_populates='employee')
    fosc01: Mapped[list['Fosc01']] = relationship('Fosc01', back_populates='employee')
    fosp01: Mapped[list['Fosp01']] = relationship('Fosp01', back_populates='employee')
    vehicles: Mapped[list['Vehicles']] = relationship('Vehicles', back_populates='employee')
    foir02: Mapped[list['Foir02']] = relationship('Foir02', foreign_keys='[Foir02.employee_id]', back_populates='employee')
    foir02_: Mapped[list['Foir02']] = relationship('Foir02', foreign_keys='[Foir02.supervisor_id]', back_populates='supervisor')
    fopp02: Mapped[list['Fopp02']] = relationship('Fopp02', back_populates='employee')
    foro05: Mapped[list['Foro05']] = relationship('Foro05', foreign_keys='[Foro05.employee_id]', back_populates='employee')
    foro05_: Mapped[list['Foro05']] = relationship('Foro05', foreign_keys='[Foro05.supervisor_id]', back_populates='supervisor')


class Equipment(Base):
    __tablename__ = 'equipment'
    __table_args__ = (
        ForeignKeyConstraint(['brand_id'], ['equipment_brands.id'], name='equipment_brand_id_fkey'),
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='equipment_client_id_fkey'),
        ForeignKeyConstraint(['type_id'], ['equipment_types.id'], name='equipment_type_id_fkey'),
        PrimaryKeyConstraint('id', name='equipment_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    type_id: Mapped[Optional[int]] = mapped_column(Integer)
    brand_id: Mapped[Optional[int]] = mapped_column(Integer)
    model: Mapped[Optional[str]] = mapped_column(String(100))
    mast: Mapped[Optional[str]] = mapped_column(String(50))
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    doh: Mapped[Optional[float]] = mapped_column(REAL)
    economic_number: Mapped[Optional[str]] = mapped_column(String(50))
    capacity: Mapped[Optional[str]] = mapped_column(String(255))
    addition: Mapped[Optional[str]] = mapped_column(String(50))
    motor: Mapped[Optional[str]] = mapped_column(String(50))
    property: Mapped[Optional[str]] = mapped_column(String(20))

    brand: Mapped[Optional['EquipmentBrands']] = relationship('EquipmentBrands', back_populates='equipment')
    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='equipment')
    type: Mapped[Optional['EquipmentTypes']] = relationship('EquipmentTypes', back_populates='equipment')
    fobc01: Mapped[list['Fobc01']] = relationship('Fobc01', back_populates='equipment')
    focr02: Mapped[list['Focr02']] = relationship('Focr02', back_populates='equipment')
    foem01: Mapped[list['Foem01']] = relationship('Foem01', back_populates='equipment')
    foim01: Mapped[list['Foim01']] = relationship('Foim01', back_populates='equipment')
    foim03: Mapped[list['Foim03']] = relationship('Foim03', back_populates='equipment')
    fole01: Mapped[list['Fole01']] = relationship('Fole01', back_populates='equipment')
    foos01: Mapped[list['Foos01']] = relationship('Foos01', back_populates='equipment')
    fopc02: Mapped[list['Fopc02']] = relationship('Fopc02', back_populates='equipment')
    fosc01: Mapped[list['Fosc01']] = relationship('Fosc01', back_populates='equipment')
    fosp01: Mapped[list['Fosp01']] = relationship('Fosp01', back_populates='equipment')
    leasing_equipment: Mapped[list['LeasingEquipment']] = relationship('LeasingEquipment', back_populates='equipment')
    foro05_services: Mapped[list['Foro05Services']] = relationship('Foro05Services', back_populates='equipment_')


class Files(Base):
    __tablename__ = 'files'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='files_client_id_fkey'),
        PrimaryKeyConstraint('id', name='files_pkey')
    )

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    status: Mapped[Optional[str]] = mapped_column(String(20))
    date_closed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    date_invoiced: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    folio_invoice: Mapped[Optional[str]] = mapped_column(String(250))
    uuid: Mapped[Optional[str]] = mapped_column(String(250))
    folio: Mapped[Optional[str]] = mapped_column(String(100))

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='files')
    fobc01: Mapped[list['Fobc01']] = relationship('Fobc01', back_populates='file')
    focr02: Mapped[list['Focr02']] = relationship('Focr02', back_populates='file')
    foem01: Mapped[list['Foem01']] = relationship('Foem01', back_populates='file')
    foem01_1: Mapped[list['Foem011']] = relationship('Foem011', back_populates='file')
    foos01: Mapped[list['Foos01']] = relationship('Foos01', back_populates='file')
    fosc01: Mapped[list['Fosc01']] = relationship('Fosc01', back_populates='file')
    fosp01: Mapped[list['Fosp01']] = relationship('Fosp01', back_populates='file')
    foro05_services: Mapped[list['Foro05Services']] = relationship('Foro05Services', back_populates='file')


class Fobc01(Base):
    __tablename__ = 'fobc01'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_fobc01_client_id'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fobc01_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='fobc01_equipment_id_fkey'),
        ForeignKeyConstraint(['file_id'], ['files.id'], name='fobc01_file_id_fkey'),
        PrimaryKeyConstraint('id', name='fobc01_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    file_id: Mapped[Optional[str]] = mapped_column(String(100))
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    observations: Mapped[Optional[str]] = mapped_column(String(300))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    reception_name: Mapped[Optional[str]] = mapped_column(String(150))
    signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    date_signed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    doh: Mapped[Optional[float]] = mapped_column(REAL)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    rating_comment: Mapped[Optional[str]] = mapped_column(String(250))
    client_id: Mapped[Optional[int]] = mapped_column(Integer)

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='fobc01')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='fobc01')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='fobc01')
    file: Mapped[Optional['Files']] = relationship('Files', back_populates='fobc01')


class Focr02(Base):
    __tablename__ = 'focr02'
    __table_args__ = (
        ForeignKeyConstraint(['additional_equipment_id'], ['focr_add_equipment.id'], name='focr02_additional_equipment_id_fkey'),
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='focr02_client_id_fkey'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='focr02_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='focr02_equipment_id_fkey'),
        ForeignKeyConstraint(['file_id'], ['files.id'], name='focr02_file_id_fkey'),
        PrimaryKeyConstraint('id', name='focr02_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    file_id: Mapped[Optional[str]] = mapped_column(String(100))
    additional_equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    reception_name: Mapped[Optional[str]] = mapped_column(String(150))
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    status: Mapped[Optional[str]] = mapped_column(String(20))
    signature_path: Mapped[Optional[str]] = mapped_column(String(150))
    date_signed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    additional_equipment: Mapped[Optional['FocrAddEquipment']] = relationship('FocrAddEquipment', back_populates='focr02')
    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='focr02')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='focr02')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='focr02')
    file: Mapped[Optional['Files']] = relationship('Files', back_populates='focr02')


class Foem01(Base):
    __tablename__ = 'foem01'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_foem01_client_id'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='foem01_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='foem01_equipment_id_fkey'),
        ForeignKeyConstraint(['file_id'], ['files.id'], name='foem01_file_id_fkey'),
        PrimaryKeyConstraint('id', name='foem01_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    file_id: Mapped[Optional[str]] = mapped_column(String(100))
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    reception_name: Mapped[Optional[str]] = mapped_column(String(150))
    signature_path: Mapped[Optional[str]] = mapped_column(String(100))
    date_signed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='foem01')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='foem01')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='foem01')
    file: Mapped[Optional['Files']] = relationship('Files', back_populates='foem01')
    foem01_materials: Mapped[list['Foem01Materials']] = relationship('Foem01Materials', back_populates='foem01')


class Foem011(Base):
    __tablename__ = 'foem01_1'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='foem01_1_client_id_fkey'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='foem01_1_employee_id_fkey'),
        ForeignKeyConstraint(['file_id'], ['files.id'], name='foem01_1_file_id_fkey'),
        PrimaryKeyConstraint('id', name='foem01_1_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    file_id: Mapped[Optional[str]] = mapped_column(String(100))
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    reception_name: Mapped[Optional[str]] = mapped_column(String(150))
    signature_path: Mapped[Optional[str]] = mapped_column(String(100))
    date_signed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='foem01_1')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='foem01_1')
    file: Mapped[Optional['Files']] = relationship('Files', back_populates='foem01_1')
    foem01_1_materials: Mapped[list['Foem011Materials']] = relationship('Foem011Materials', back_populates='foem01_1')


class Foim01(Base):
    __tablename__ = 'foim01'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_foim01_client_id'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='foim01_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='foim01_equipment_id_fkey'),
        PrimaryKeyConstraint('id', name='foim01_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    hourometer: Mapped[Optional[str]] = mapped_column(String(50))
    observations: Mapped[Optional[str]] = mapped_column(String(500))
    reception_name: Mapped[Optional[str]] = mapped_column(String(100))
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    status: Mapped[Optional[str]] = mapped_column(String(20))
    signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    date_signed: Mapped[Optional[datetime.date]] = mapped_column(Date)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    rating_comment: Mapped[Optional[str]] = mapped_column(String(250))
    client_id: Mapped[Optional[int]] = mapped_column(Integer)

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='foim01')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='foim01')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='foim01')
    foim01_answers: Mapped[list['Foim01Answers']] = relationship('Foim01Answers', back_populates='foim01')


class Foim03(Base):
    __tablename__ = 'foim03'
    __table_args__ = (
        ForeignKeyConstraint(['app_user_id'], ['app_users.id'], name='foim03_app_user_id_fkey'),
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_foim01_client_id'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='foim03_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='foim03_equipment_id_fkey'),
        PrimaryKeyConstraint('id', name='foim03_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    app_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    status: Mapped[Optional[str]] = mapped_column(String(20))
    client_id: Mapped[Optional[int]] = mapped_column(Integer)

    app_user: Mapped[Optional['AppUsers']] = relationship('AppUsers', back_populates='foim03')
    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='foim03')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='foim03')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='foim03')
    foim03_answers: Mapped[list['Foim03Answers']] = relationship('Foim03Answers', back_populates='foim03')


class Fole01(Base):
    __tablename__ = 'fole01'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE', onupdate='CASCADE', name='client_fole01_fk'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fole01_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='fole01_equipment_id_fkey'),
        PrimaryKeyConstraint('id', name='fole01_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    technical_action: Mapped[Optional[str]] = mapped_column(String(750))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    reception_name: Mapped[Optional[str]] = mapped_column(String(150))
    signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    date_signed: Mapped[Optional[datetime.date]] = mapped_column(Date)
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    rating_comment: Mapped[Optional[str]] = mapped_column(String(250))
    client_id: Mapped[Optional[int]] = mapped_column(Integer)

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='fole01')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='fole01')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='fole01')
    fole01_services: Mapped[list['Fole01Services']] = relationship('Fole01Services', back_populates='fole01')


class Foos01(Base):
    __tablename__ = 'foos01'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_foos01_client_id'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='foos01_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='foos01_equipment_id_fkey'),
        ForeignKeyConstraint(['file_id'], ['files.id'], name='fk_foos01_files'),
        ForeignKeyConstraint(['fopc_services_id'], ['fopc_services.id'], name='foos01_fopc_services_id_fkey'),
        PrimaryKeyConstraint('id', name='foos01_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    file_id: Mapped[Optional[str]] = mapped_column(String(100))
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    observations: Mapped[Optional[str]] = mapped_column(String(300))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    reception_name: Mapped[Optional[str]] = mapped_column(String(150))
    signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    date_signed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    rating_comment: Mapped[Optional[str]] = mapped_column(String(250))
    fopc_services_id: Mapped[Optional[int]] = mapped_column(Integer)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    GC: Mapped[Optional[str]] = mapped_column(String(20))


    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='foos01')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='foos01')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='foos01')
    file: Mapped[Optional['Files']] = relationship('Files', back_populates='foos01')
    fopc_services: Mapped[Optional['FopcServices']] = relationship('FopcServices', back_populates='foos01')
    foos01_services: Mapped[list['Foos01Services']] = relationship('Foos01Services', back_populates='foos01')


class Fopc02(Base):
    __tablename__ = 'fopc02'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fopc02_client_id_fkey'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fopc02_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='fopc02_equipment_id_fkey'),
        ForeignKeyConstraint(['fopc_services_id'], ['fopc_services.id'], name='fopc02_fopc_services_id_fkey'),
        ForeignKeyConstraint(['property_id'], ['client_equipment_property.id'], name='fopc02_property_id_fkey'),
        PrimaryKeyConstraint('id', name='fopc02_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    property_id: Mapped[Optional[int]] = mapped_column(Integer)
    departure_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    departure_description: Mapped[Optional[str]] = mapped_column(String(300))
    return_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    return_description: Mapped[Optional[str]] = mapped_column(String(300))
    exit_signature_path: Mapped[Optional[str]] = mapped_column(String(100))
    exit_employee_signature_path: Mapped[Optional[str]] = mapped_column(String(100))
    return_signature_path: Mapped[Optional[str]] = mapped_column(String(100))
    return_employee_signature_path: Mapped[Optional[str]] = mapped_column(String(100))
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(20))
    name_auth_departure: Mapped[Optional[str]] = mapped_column(String(100))
    name_recipient: Mapped[Optional[str]] = mapped_column(String(100))
    observations: Mapped[Optional[str]] = mapped_column(String(300))
    fopc_services_id: Mapped[Optional[int]] = mapped_column(Integer)

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='fopc02')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='fopc02')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='fopc02')
    fopc_services: Mapped[Optional['FopcServices']] = relationship('FopcServices', back_populates='fopc02')
    property: Mapped[Optional['ClientEquipmentProperty']] = relationship('ClientEquipmentProperty', back_populates='fopc02')
    fopp02: Mapped[list['Fopp02']] = relationship('Fopp02', back_populates='fopc')


class Fosc01(Base):
    __tablename__ = 'fosc01'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_fosc01_client_id'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fosc01_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='fosc01_equipment_id_fkey'),
        ForeignKeyConstraint(['file_id'], ['files.id'], name='fosc01_file_id_fkey'),
        ForeignKeyConstraint(['fopc_services_id'], ['fopc_services.id'], name='fosc01_fopc_services_id_fkey'),
        PrimaryKeyConstraint('id', name='fosc01_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    file_id: Mapped[Optional[str]] = mapped_column(String(100))
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    observations: Mapped[Optional[str]] = mapped_column(String(1000))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    reception_name: Mapped[Optional[str]] = mapped_column(String(150))
    signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    date_signed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    rating_comment: Mapped[Optional[str]] = mapped_column(String(250))
    fopc_services_id: Mapped[Optional[int]] = mapped_column(Integer)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    GC: Mapped[Optional[str]] = mapped_column(String(20))

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='fosc01')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='fosc01')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='fosc01')
    file: Mapped[Optional['Files']] = relationship('Files', back_populates='fosc01')
    fopc_services: Mapped[Optional['FopcServices']] = relationship('FopcServices', back_populates='fosc01')
    fosc01_services: Mapped[list['Fosc01Services']] = relationship('Fosc01Services', back_populates='fosc01')


class Fosp01(Base):
    __tablename__ = 'fosp01'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_fosp01_client_id'),
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fosp01_employee_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='fosp01_equipment_id_fkey'),
        ForeignKeyConstraint(['file_id'], ['files.id'], name='fosp01_file_id_fkey'),
        ForeignKeyConstraint(['fopc_services_id'], ['fopc_services.id'], name='fosp01_fopc_services_id_fkey'),
        PrimaryKeyConstraint('id', name='fosp01_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    file_id: Mapped[Optional[str]] = mapped_column(String(100))
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    hourometer: Mapped[Optional[float]] = mapped_column(REAL)
    observations: Mapped[Optional[str]] = mapped_column(String(1000))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    reception_name: Mapped[Optional[str]] = mapped_column(String(150))
    signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    date_signed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    rating_comment: Mapped[Optional[str]] = mapped_column(String(250))
    fopc_services_id: Mapped[Optional[int]] = mapped_column(Integer)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    GC: Mapped[Optional[str]] = mapped_column(String(20))


    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='fosp01')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='fosp01')
    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='fosp01')
    file: Mapped[Optional['Files']] = relationship('Files', back_populates='fosp01')
    fopc_services: Mapped[Optional['FopcServices']] = relationship('FopcServices', back_populates='fosp01')
    fosp01_services: Mapped[list['Fosp01Services']] = relationship('Fosp01Services', back_populates='fosp01')


class LeasingEquipment(Base):
    __tablename__ = 'leasing_equipment'
    __table_args__ = (
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='leasing_equipment_equipment_id_fkey'),
        PrimaryKeyConstraint('id', name='leasing_equipment_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    img_path: Mapped[Optional[str]] = mapped_column(String(100))
    technical_sheet_path: Mapped[Optional[str]] = mapped_column(String(100))
    price: Mapped[Optional[float]] = mapped_column(REAL)
    type: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[Optional[str]] = mapped_column(String(50))

    equipment: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='leasing_equipment')


class Vehicles(Base):
    __tablename__ = 'vehicles'
    __table_args__ = (
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='vehicles_employee_id_fkey'),
        PrimaryKeyConstraint('id', name='vehicles_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(30))
    license_plate: Mapped[Optional[str]] = mapped_column(String(15))
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)

    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='vehicles')
    foir02: Mapped[list['Foir02']] = relationship('Foir02', back_populates='vehicle')
    foro05: Mapped[list['Foro05']] = relationship('Foro05', back_populates='vehicle')


class Foem011Materials(Base):
    __tablename__ = 'foem01_1_materials'
    __table_args__ = (
        ForeignKeyConstraint(['foem01_1_id'], ['foem01_1.id'], name='foem01_1_materials_foem01_1_id_fkey'),
        PrimaryKeyConstraint('id', name='foem01_1_materials_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    foem01_1_id: Mapped[Optional[int]] = mapped_column(Integer)
    amount: Mapped[Optional[int]] = mapped_column(Integer)
    um: Mapped[Optional[str]] = mapped_column(String(50))
    part_number: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(200))

    foem01_1: Mapped[Optional['Foem011']] = relationship('Foem011', back_populates='foem01_1_materials')


class Foem01Materials(Base):
    __tablename__ = 'foem01_materials'
    __table_args__ = (
        ForeignKeyConstraint(['foem01_id'], ['foem01.id'], name='foem01_materials_foem01_id_fkey'),
        PrimaryKeyConstraint('id', name='foem01_materials_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    foem01_id: Mapped[Optional[int]] = mapped_column(Integer)
    amount: Mapped[Optional[int]] = mapped_column(Integer)
    um: Mapped[Optional[str]] = mapped_column(String(50))
    part_number: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(200))

    foem01: Mapped[Optional['Foem01']] = relationship('Foem01', back_populates='foem01_materials')


class Foim01Answers(Base):
    __tablename__ = 'foim01_answers'
    __table_args__ = (
        ForeignKeyConstraint(['foim01_id'], ['foim01.id'], name='foim01_answers_foim01_id_fkey'),
        ForeignKeyConstraint(['foim_question_id'], ['foim_questions.id'], name='foim01_answers_foim_question_id_fkey'),
        PrimaryKeyConstraint('id', name='foim01_answers_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    foim_question_id: Mapped[Optional[int]] = mapped_column(Integer)
    foim01_id: Mapped[Optional[int]] = mapped_column(Integer)
    answer: Mapped[Optional[str]] = mapped_column(String(10))
    description: Mapped[Optional[str]] = mapped_column(String(250))

    foim01: Mapped[Optional['Foim01']] = relationship('Foim01', back_populates='foim01_answers')
    foim_question: Mapped[Optional['FoimQuestions']] = relationship('FoimQuestions', back_populates='foim01_answers')


class Foim03Answers(Base):
    __tablename__ = 'foim03_answers'
    __table_args__ = (
        ForeignKeyConstraint(['foim03_id'], ['foim03.id'], name='foim03_answers_foim03_id_fkey'),
        ForeignKeyConstraint(['foim_question_id'], ['foim_questions.id'], name='foim03_answers_foim_question_id_fkey'),
        PrimaryKeyConstraint('id', name='foim03_answers_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    foim_question_id: Mapped[Optional[int]] = mapped_column(Integer)
    foim03_id: Mapped[Optional[int]] = mapped_column(Integer)
    answer: Mapped[Optional[str]] = mapped_column(String(10))
    description: Mapped[Optional[str]] = mapped_column(String(250))
    status: Mapped[Optional[str]] = mapped_column(String(50))

    foim03: Mapped[Optional['Foim03']] = relationship('Foim03', back_populates='foim03_answers')
    foim_question: Mapped[Optional['FoimQuestions']] = relationship('FoimQuestions', back_populates='foim03_answers')


class Foir02(Base):
    __tablename__ = 'foir02'
    __table_args__ = (
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='foir02_employee_id_fkey'),
        ForeignKeyConstraint(['supervisor_id'], ['employees.id'], name='foir02_supervisor_id_fkey'),
        ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], name='foir02_vehicle_id_fkey'),
        PrimaryKeyConstraint('id', name='foir02_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[Optional[str]] = mapped_column(String(10))
    vehicle_id: Mapped[Optional[int]] = mapped_column(Integer)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    supervisor_id: Mapped[Optional[int]] = mapped_column(Integer)
    date_route: Mapped[Optional[datetime.date]] = mapped_column(Date)
    employee_signature_path: Mapped[Optional[str]] = mapped_column(String(300))
    supervisor_signature_path: Mapped[Optional[str]] = mapped_column(String(300))

    employee: Mapped[Optional['Employees']] = relationship('Employees', foreign_keys=[employee_id], back_populates='foir02')
    supervisor: Mapped[Optional['Employees']] = relationship('Employees', foreign_keys=[supervisor_id], back_populates='foir02_')
    vehicle: Mapped[Optional['Vehicles']] = relationship('Vehicles', back_populates='foir02')
    foir02_equipment_checklist: Mapped[list['Foir02EquipmentChecklist']] = relationship('Foir02EquipmentChecklist', back_populates='foir')


class Fole01Services(Base):
    __tablename__ = 'fole01_services'
    __table_args__ = (
        ForeignKeyConstraint(['fole01_id'], ['fole01.id'], name='fole01_services_fole01_id_fkey'),
        ForeignKeyConstraint(['service_id'], ['services.id'], name='fole01_services_service_id_fkey'),
        PrimaryKeyConstraint('id', name='fole01_services_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fole01_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_id: Mapped[Optional[int]] = mapped_column(Integer)
    diagnose_description: Mapped[Optional[str]] = mapped_column(String(550))
    description_service: Mapped[Optional[str]] = mapped_column(String(550))
    priority: Mapped[Optional[str]] = mapped_column(String(50))

    fole01: Mapped[Optional['Fole01']] = relationship('Fole01', back_populates='fole01_services')
    service: Mapped[Optional['Services']] = relationship('Services', back_populates='fole01_services')


class Foos01Services(Base):
    __tablename__ = 'foos01_services'
    __table_args__ = (
        ForeignKeyConstraint(['foos01_id'], ['foos01.id'], name='foos01_services_foos01_id_fkey'),
        ForeignKeyConstraint(['service_id'], ['services.id'], name='foos01_services_service_id_fkey'),
        PrimaryKeyConstraint('id', name='foos01_services_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    foos01_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_description: Mapped[Optional[str]] = mapped_column(String(599))

    foos01: Mapped[Optional['Foos01']] = relationship('Foos01', back_populates='foos01_services')
    service: Mapped[Optional['Services']] = relationship('Services', back_populates='foos01_services')


class Fopp02(Base):
    __tablename__ = 'fopp02'
    __table_args__ = (
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fopp02_employee_id_fkey'),
        ForeignKeyConstraint(['fopc_id'], ['fopc02.id'], name='fopp02_fopc_id_fkey'),
        ForeignKeyConstraint(['property_id'], ['client_equipment_property.id'], name='fopp02_property_id_fkey'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], name='fopp02_vendor_id_fkey'),
        PrimaryKeyConstraint('id', name='fopp02_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vendor_id: Mapped[Optional[int]] = mapped_column(Integer)
    property_id: Mapped[Optional[int]] = mapped_column(Integer)
    departure_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    departure_description: Mapped[Optional[str]] = mapped_column(String(300))
    delivery_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    delivery_description: Mapped[Optional[str]] = mapped_column(String(300))
    departure_signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    departure_employee_signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    delivery_signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    delivery_employee_signature_path: Mapped[Optional[str]] = mapped_column(String(50))
    observations: Mapped[Optional[str]] = mapped_column(String(300))
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(20))
    name_auth_departure: Mapped[Optional[str]] = mapped_column(String(100))
    name_delivery: Mapped[Optional[str]] = mapped_column(String(100))
    fopc_id: Mapped[Optional[int]] = mapped_column(Integer)

    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='fopp02')
    fopc: Mapped[Optional['Fopc02']] = relationship('Fopc02', back_populates='fopp02')
    property: Mapped[Optional['ClientEquipmentProperty']] = relationship('ClientEquipmentProperty', back_populates='fopp02')
    vendor: Mapped[Optional['Vendors']] = relationship('Vendors', back_populates='fopp02')


class Foro05(Base):
    __tablename__ = 'foro05'
    __table_args__ = (
        ForeignKeyConstraint(['employee_id'], ['employees.id'], name='foro02_employee_id_fkey'),
        ForeignKeyConstraint(['supervisor_id'], ['employees.id'], name='foro02_supervisor_id_fkey'),
        ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], name='foro02_vehicle_id_fkey'),
        PrimaryKeyConstraint('id', name='foro02_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('foro02_id_seq'), primary_key=True)
    status: Mapped[Optional[str]] = mapped_column(String(10))
    vehicle_id: Mapped[Optional[int]] = mapped_column(Integer)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer)
    supervisor_id: Mapped[Optional[int]] = mapped_column(Integer)
    route_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    comments: Mapped[Optional[str]] = mapped_column(String(300))
    signature_path_employee: Mapped[Optional[str]] = mapped_column(String(300))
    signature_path_supervisor: Mapped[Optional[str]] = mapped_column(String(300))

    employee: Mapped[Optional['Employees']] = relationship('Employees', foreign_keys=[employee_id], back_populates='foro05')
    supervisor: Mapped[Optional['Employees']] = relationship('Employees', foreign_keys=[supervisor_id], back_populates='foro05_')
    vehicle: Mapped[Optional['Vehicles']] = relationship('Vehicles', back_populates='foro05')
    foro05_employee_checklist: Mapped[list['Foro05EmployeeChecklist']] = relationship('Foro05EmployeeChecklist', back_populates='foro05')
    foro05_services: Mapped[list['Foro05Services']] = relationship('Foro05Services', back_populates='foro')
    foro05_vehicle_checklist: Mapped[list['Foro05VehicleChecklist']] = relationship('Foro05VehicleChecklist', back_populates='foro05')


class Fosc01Services(Base):
    __tablename__ = 'fosc01_services'
    __table_args__ = (
        ForeignKeyConstraint(['fosc01_id'], ['fosc01.id'], name='fosc01_services_fosc01_id_fkey'),
        ForeignKeyConstraint(['service_id'], ['services.id'], name='fosc01_services_service_id_fkey'),
        PrimaryKeyConstraint('id', name='fosc01_services_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fosc01_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_description: Mapped[Optional[str]] = mapped_column(String(599))

    fosc01: Mapped[Optional['Fosc01']] = relationship('Fosc01', back_populates='fosc01_services')
    service: Mapped[Optional['Services']] = relationship('Services', back_populates='fosc01_services')


class Fosp01Services(Base):
    __tablename__ = 'fosp01_services'
    __table_args__ = (
        ForeignKeyConstraint(['fosp01_id'], ['fosp01.id'], name='fosp01_services_fosp01_id_fkey'),
        ForeignKeyConstraint(['service_id'], ['services.id'], name='fosp01_services_service_id_fkey'),
        PrimaryKeyConstraint('id', name='fosp01_services_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fosp01_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_id: Mapped[Optional[int]] = mapped_column(Integer)

    fosp01: Mapped[Optional['Fosp01']] = relationship('Fosp01', back_populates='fosp01_services')
    service: Mapped[Optional['Services']] = relationship('Services', back_populates='fosp01_services')


class Foir02EquipmentChecklist(Base):
    __tablename__ = 'foir02_equipment_checklist'
    __table_args__ = (
        ForeignKeyConstraint(['equipment_id'], ['foir02_requiered_equipment.id'], name='foir02_equipment_checlist_equipment_id_fkey'),
        ForeignKeyConstraint(['foir_id'], ['foir02.id'], name='foir02_equipment_checlist_foir_id_fkey'),
        PrimaryKeyConstraint('id', name='foir02_equipment_checlist_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('foir02_equipment_checlist_id_seq'), primary_key=True)
    foir_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[bool]] = mapped_column(Boolean)
    comments: Mapped[Optional[str]] = mapped_column(String(200))

    equipment: Mapped[Optional['Foir02RequieredEquipment']] = relationship('Foir02RequieredEquipment', back_populates='foir02_equipment_checklist')
    foir: Mapped[Optional['Foir02']] = relationship('Foir02', back_populates='foir02_equipment_checklist')


class Foro05EmployeeChecklist(Base):
    __tablename__ = 'foro05_employee_checklist'
    __table_args__ = (
        ForeignKeyConstraint(['foro05_id'], ['foro05.id'], name='foro05_employee_checklist_foro05_id_fkey'),
        PrimaryKeyConstraint('id', name='foro05_employee_checklist_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    foro05_id: Mapped[Optional[int]] = mapped_column(Integer)
    neat: Mapped[Optional[bool]] = mapped_column(Boolean)
    full_uniform: Mapped[Optional[bool]] = mapped_column(Boolean)
    clean_uniform: Mapped[Optional[bool]] = mapped_column(Boolean)
    safty_boots: Mapped[Optional[bool]] = mapped_column(Boolean)
    ddg_id: Mapped[Optional[bool]] = mapped_column(Boolean)
    valid_license: Mapped[Optional[bool]] = mapped_column(Boolean)
    presentation_card: Mapped[Optional[bool]] = mapped_column(Boolean)

    foro05: Mapped[Optional['Foro05']] = relationship('Foro05', back_populates='foro05_employee_checklist')


class Foro05Services(Base):
    __tablename__ = 'foro05_services'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='foro05_services_client_id_fkey'),
        ForeignKeyConstraint(['equipment_id'], ['equipment.id'], name='foro05_services_equipment_id_fkey'),
        ForeignKeyConstraint(['file_id'], ['files.id'], name='foro05_services_file_id_fkey'),
        ForeignKeyConstraint(['foro_id'], ['foro05.id'], name='foro05_services_foro_id_fkey'),
        ForeignKeyConstraint(['service_id'], ['services.id'], name='foro05_services_service_id_fkey'),
        PrimaryKeyConstraint('id', name='foro05_services_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    foro_id: Mapped[Optional[int]] = mapped_column(Integer)
    client_id: Mapped[Optional[int]] = mapped_column(Integer)
    equipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    service_id: Mapped[Optional[int]] = mapped_column(Integer)
    file_id: Mapped[Optional[str]] = mapped_column(String(150))
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    equipment: Mapped[Optional[str]] = mapped_column(String(50))

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='foro05_services')
    equipment_: Mapped[Optional['Equipment']] = relationship('Equipment', back_populates='foro05_services')
    file: Mapped[Optional['Files']] = relationship('Files', back_populates='foro05_services')
    foro: Mapped[Optional['Foro05']] = relationship('Foro05', back_populates='foro05_services')
    service: Mapped[Optional['Services']] = relationship('Services', back_populates='foro05_services')
    foro05_service_suplies: Mapped[list['Foro05ServiceSuplies']] = relationship('Foro05ServiceSuplies', back_populates='foro05_service')


class Foro05VehicleChecklist(Base):
    __tablename__ = 'foro05_vehicle_checklist'
    __table_args__ = (
        ForeignKeyConstraint(['foro05_id'], ['foro05.id'], name='foro05_vehicle_cheklist_foro05_id_fkey'),
        PrimaryKeyConstraint('id', name='foro05_vehicle_cheklist_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('foro05_vehicle_cheklist_id_seq'), primary_key=True)
    foro05_id: Mapped[Optional[int]] = mapped_column(Integer)
    checklist: Mapped[Optional[bool]] = mapped_column(Boolean)
    clean_tools: Mapped[Optional[bool]] = mapped_column(Boolean)
    tidy_tools: Mapped[Optional[bool]] = mapped_column(Boolean)
    clean_vehicle: Mapped[Optional[bool]] = mapped_column(Boolean)
    tidy_vehicle: Mapped[Optional[bool]] = mapped_column(Boolean)
    fuel: Mapped[Optional[bool]] = mapped_column(Boolean)
    documents: Mapped[Optional[bool]] = mapped_column(Boolean)

    foro05: Mapped[Optional['Foro05']] = relationship('Foro05', back_populates='foro05_vehicle_checklist')


class Foro05ServiceSuplies(Base):
    __tablename__ = 'foro05_service_suplies'
    __table_args__ = (
        ForeignKeyConstraint(['foro05_service_id'], ['foro05_services.id'], name='foro05_service_suplies_foro05_service_id_fkey'),
        PrimaryKeyConstraint('id', name='foro05_service_suplies_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    foro05_service_id: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(String(30))
    status: Mapped[Optional[bool]] = mapped_column(Boolean)

    foro05_service: Mapped[Optional['Foro05Services']] = relationship('Foro05Services', back_populates='foro05_service_suplies')
