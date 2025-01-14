"""empty message

Revision ID: 83cf2bb05d46
Revises: ba758463622a
Create Date: 2023-09-03 17:28:07.674455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83cf2bb05d46'
down_revision = 'ba758463622a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('personajes', schema=None) as batch_op:
        batch_op.drop_constraint('personajes_birth_year_key', type_='unique')
        batch_op.drop_constraint('personajes_eye_color_key', type_='unique')
        batch_op.drop_constraint('personajes_gender_key', type_='unique')
        batch_op.drop_constraint('personajes_hair_color_key', type_='unique')
        batch_op.drop_constraint('personajes_height_key', type_='unique')
        batch_op.drop_constraint('personajes_mass_key', type_='unique')
        batch_op.drop_constraint('personajes_skin_color_key', type_='unique')

    with op.batch_alter_table('planetas', schema=None) as batch_op:
        batch_op.drop_constraint('planetas_climate_key', type_='unique')
        batch_op.drop_constraint('planetas_diameter_key', type_='unique')
        batch_op.drop_constraint('planetas_gravity_key', type_='unique')
        batch_op.drop_constraint('planetas_orbital_period_key', type_='unique')
        batch_op.drop_constraint('planetas_population_key', type_='unique')
        batch_op.drop_constraint('planetas_rotation_period_key', type_='unique')
        batch_op.drop_constraint('planetas_surface_water_key', type_='unique')
        batch_op.drop_constraint('planetas_terrain_key', type_='unique')

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_constraint('usuario_apellido_key', type_='unique')
        batch_op.drop_constraint('usuario_nombre_key', type_='unique')

    with op.batch_alter_table('vehiculos', schema=None) as batch_op:
        batch_op.drop_constraint('vehiculos_cargo_capacity_key', type_='unique')
        batch_op.drop_constraint('vehiculos_consumables_key', type_='unique')
        batch_op.drop_constraint('vehiculos_cost_in_credits_key', type_='unique')
        batch_op.drop_constraint('vehiculos_crew_key', type_='unique')
        batch_op.drop_constraint('vehiculos_films_key', type_='unique')
        batch_op.drop_constraint('vehiculos_length_key', type_='unique')
        batch_op.drop_constraint('vehiculos_manufacturer_key', type_='unique')
        batch_op.drop_constraint('vehiculos_max_atmosphering_speed_key', type_='unique')
        batch_op.drop_constraint('vehiculos_passengers_key', type_='unique')
        batch_op.drop_constraint('vehiculos_pilots_key', type_='unique')
        batch_op.drop_constraint('vehiculos_vehicle_class_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehiculos', schema=None) as batch_op:
        batch_op.create_unique_constraint('vehiculos_vehicle_class_key', ['vehicle_class'])
        batch_op.create_unique_constraint('vehiculos_pilots_key', ['pilots'])
        batch_op.create_unique_constraint('vehiculos_passengers_key', ['passengers'])
        batch_op.create_unique_constraint('vehiculos_max_atmosphering_speed_key', ['max_atmosphering_speed'])
        batch_op.create_unique_constraint('vehiculos_manufacturer_key', ['manufacturer'])
        batch_op.create_unique_constraint('vehiculos_length_key', ['length'])
        batch_op.create_unique_constraint('vehiculos_films_key', ['films'])
        batch_op.create_unique_constraint('vehiculos_crew_key', ['crew'])
        batch_op.create_unique_constraint('vehiculos_cost_in_credits_key', ['cost_in_credits'])
        batch_op.create_unique_constraint('vehiculos_consumables_key', ['consumables'])
        batch_op.create_unique_constraint('vehiculos_cargo_capacity_key', ['cargo_capacity'])

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.create_unique_constraint('usuario_nombre_key', ['nombre'])
        batch_op.create_unique_constraint('usuario_apellido_key', ['apellido'])

    with op.batch_alter_table('planetas', schema=None) as batch_op:
        batch_op.create_unique_constraint('planetas_terrain_key', ['terrain'])
        batch_op.create_unique_constraint('planetas_surface_water_key', ['surface_water'])
        batch_op.create_unique_constraint('planetas_rotation_period_key', ['rotation_period'])
        batch_op.create_unique_constraint('planetas_population_key', ['population'])
        batch_op.create_unique_constraint('planetas_orbital_period_key', ['orbital_period'])
        batch_op.create_unique_constraint('planetas_gravity_key', ['gravity'])
        batch_op.create_unique_constraint('planetas_diameter_key', ['diameter'])
        batch_op.create_unique_constraint('planetas_climate_key', ['climate'])

    with op.batch_alter_table('personajes', schema=None) as batch_op:
        batch_op.create_unique_constraint('personajes_skin_color_key', ['skin_color'])
        batch_op.create_unique_constraint('personajes_mass_key', ['mass'])
        batch_op.create_unique_constraint('personajes_height_key', ['height'])
        batch_op.create_unique_constraint('personajes_hair_color_key', ['hair_color'])
        batch_op.create_unique_constraint('personajes_gender_key', ['gender'])
        batch_op.create_unique_constraint('personajes_eye_color_key', ['eye_color'])
        batch_op.create_unique_constraint('personajes_birth_year_key', ['birth_year'])

    # ### end Alembic commands ###
