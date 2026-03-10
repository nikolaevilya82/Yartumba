"""
Тесты материалов (SheetMaterial, EdgeMaterial, фурнитура)
"""
import pytest
from app.models.materials import (
    SheetMaterial,
    EdgeMaterial,
    SlideGuide,
    Hinge,
    Support,
    WallMount,
)


class TestSheetMaterial:
    def test_create_sheet_material(self, db_session):
        """Создание листового материала"""
        sheet = SheetMaterial(
            name="ДСП 16мм Дуб сонома",
            material_type="ldsp",
            thickness=16,
            standard_width=2800,
            standard_height=2070,
            decor_name="Дуб сонома",
            price=3500
        )
        db_session.add(sheet)
        db_session.commit()
        
        assert sheet.id is not None
        assert sheet.material_type == "ldsp"
        assert sheet.thickness == 16
        assert sheet.decor_name == "Дуб сонома"

    def test_sheet_material_types(self, db_session):
        """Все типы материалов"""
        materials = [
            ("ДСП 16мм", "chipboard"),
            ("ЛДСП 16мм", "ldsp"),
            ("МДФ 18мм", "mdf"),
            ("ХДФ 6мм", "hdf"),
            ("Фанера 12мм", "plywood"),
            ("Массив дуба", "solid_wood"),
        ]
        
        for name, mat_type in materials:
            sheet = SheetMaterial(
                name=name,
                material_type=mat_type,
                thickness=16,
                standard_width=2800,
                standard_height=2070,
                price=1000
            )
            db_session.add(sheet)
        
        db_session.commit()
        
        sheets = db_session.query(SheetMaterial).all()
        assert len(sheets) == 6


class TestEdgeMaterial:
    def test_create_edge_material(self, db_session):
        """Создание кромки"""
        sheet = SheetMaterial(
            name="ДСП 16мм Дуб сонома",
            material_type="ldsp",
            thickness=16,
            standard_width=2800,
            standard_height=2070,
            decor_name="Дуб сонома"
        )
        db_session.add(sheet)
        db_session.commit()
        
        edge = EdgeMaterial(
            sheet_material_id=sheet.id,
            edge_type="abs",
            thickness=0.5,
            width=23,
            decor_name="Дуб сонома",
            price_per_meter=50
        )
        db_session.add(edge)
        db_session.commit()
        
        assert edge.id is not None
        assert edge.edge_type == "abs"
        assert edge.sheet_material_id == sheet.id

    def test_edge_unique_constraint(self, db_session):
        """Уникальность связи 1:1"""
        sheet = SheetMaterial(
            name="ДСП 16мм",
            material_type="ldsp",
            thickness=16,
            standard_width=2800,
            standard_height=2070
        )
        db_session.add(sheet)
        db_session.commit()
        
        edge1 = EdgeMaterial(
            sheet_material_id=sheet.id,
            edge_type="abs",
            thickness=0.5,
            width=23,
            decor_name="Дуб сонома"
        )
        db_session.add(edge1)
        db_session.commit()
        
        # Попытка создать вторую кромку для того же листа
        edge2 = EdgeMaterial(
            sheet_material_id=sheet.id,
            edge_type="pvc",
            thickness=0.4,
            width=21,
            decor_name="Дуб сонома"
        )
        db_session.add(edge2)
        
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()


class TestSlideGuide:
    def test_create_slide_guide(self, db_session):
        """Создание направляющих"""
        guide = SlideGuide(
            name="Направляющие шариковые полновыкатные",
            guide_type="ball",
            extension_type="full",
            length=450,
            load_capacity=30,
            has_soft_close=True,
            price=1500
        )
        db_session.add(guide)
        db_session.commit()
        
        assert guide.id is not None
        assert guide.guide_type == "ball"
        assert guide.extension_type == "full"


class TestHinge:
    def test_create_hinge(self, db_session):
        """Создание петель"""
        hinge = Hinge(
            name="Петля Blum",
            hinge_type="clip",
            mounting_type="overlay",
            opening_angle=110,
            has_soft_close=True,
            has_integrated_soft_close=True,
            price=250
        )
        db_session.add(hinge)
        db_session.commit()
        
        assert hinge.id is not None
        assert hinge.mounting_type == "overlay"
        assert hinge.has_soft_close is True


class TestSupport:
    def test_create_support(self, db_session):
        """Создание опор"""
        support = Support(
            name="Ножка регулируемая",
            support_type="adjustable",
            material="metal",
            height=100,
            diameter=50,
            is_adjustable=True,
            price=150
        )
        db_session.add(support)
        db_session.commit()
        
        assert support.id is not None
        assert support.is_adjustable is True


class TestWallMount:
    def test_create_wall_mount(self, db_session):
        """Создание настенного крепления"""
        mount = WallMount(
            name="Навеска скрытая",
            mount_type="hanger",
            wall_type="drywall",
            max_load=50,
            adjustment="3d",
            is_hidden=True,
            price=200
        )
        db_session.add(mount)
        db_session.commit()
        
        assert mount.id is not None
        assert mount.mount_type == "hanger"
        assert mount.max_load == 50
