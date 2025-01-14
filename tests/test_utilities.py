import numpy as np
import pytest

from pythermalcomfort.utilities import (
    body_surface_area,
    clo_dynamic,
    f_svv,
    running_mean_outdoor_temperature,
    transpose_sharp_altitude,
    units_converter,
    v_relative,
    clo_intrinsic_insulation_ensemble,
    clo_area_factor,
    clo_insulation_air_layer,
    clo_total_insulation,
    clo_correction_factor_environment,
)


def test_intrinsic_insulation_ensemble():
    assert clo_intrinsic_insulation_ensemble([0.5, 0.5]) == 0.835 + 0.161
    assert clo_intrinsic_insulation_ensemble([1, 1]) == 2 * 0.835 + 0.161
    assert clo_intrinsic_insulation_ensemble(2) == 2 * 0.835 + 0.161
    assert clo_intrinsic_insulation_ensemble([0]) == 0.161


def test_clo_area_factor():
    assert clo_area_factor(1) == 1.28
    assert np.allclose(clo_area_factor(i_cl=[1, 2]), np.array([1.28, 1.56]))


def test_clo_air_layer_insulation():
    assert np.isclose(
        clo_insulation_air_layer(vr=1, v_walk=1, i_a_static=0.71), 0.365, atol=0.001
    )
    assert np.isclose(
        clo_insulation_air_layer(vr=0.2, v_walk=1, i_a_static=0.71), 0.532, atol=0.001
    )
    assert np.allclose(
        clo_insulation_air_layer(vr=[0.2, 1], v_walk=1, i_a_static=0.71),
        [0.532, 0.365],
        atol=0.001,
    )


def test_clo_total_insulation():

    # test that the normal_clothing function works as expected
    assert np.allclose(
        clo_total_insulation(
            i_t=[1.21, 1.26, 1.56],
            vr=0.15,
            v_walk=0,
            i_a_static=0.5,
            i_cl=[0.61, 0.71, 1.01],
        ),
        [1.21, 1.26, 1.56],
        atol=0.001,
    )

    # compare the normal_clothing results with the figure in the standard
    assert np.allclose(
        clo_total_insulation(
            i_t=[1.21, 1.26, 1.56],
            vr=2,
            v_walk=[1, 0.5, 0.25],
            i_a_static=0.5,
            i_cl=[0.61, 0.71, 1.01],
        ),
        [1.21 * 0.5, 1.26 * 0.565, 1.56 * 0.62],
        atol=0.005,
    )

    # test that the nude function works as expected
    assert np.allclose(
        clo_total_insulation(
            i_t=0,
            vr=0.15,
            v_walk=0,
            i_a_static=[0.71, 0.61, 0.5],
            i_cl=0,
        ),
        [0.71, 0.61, 0.5],
        atol=0.001,
    )

    # compare the nude results with the figure in the standard
    assert np.allclose(
        clo_total_insulation(
            i_t=0,
            vr=[0.5, 2, 3],
            v_walk=0.5,
            i_a_static=[0.71, 0.61, 0.5],
            i_cl=0,
        ),
        [0.71 * 0.7, 0.61 * 0.4, 0.50 * 0.32],
        atol=0.004,
    )

    # test that the low_clothing function works as expected
    assert np.allclose(
        clo_total_insulation(
            i_t=1.2,
            vr=0.15,
            v_walk=0,
            i_a_static=[0.6, 0.6],
            i_cl=[0.6, 0],
        ),
        [0.6, 0.6],
        atol=0.001,
    )


def test_clo_correction_factor_environment():

    # test that the normal_clothing function works as expected
    assert np.allclose(
        clo_correction_factor_environment(
            vr=0.15,
            v_walk=0,
            i_cl=[0.61, 0.71, 1.01],
        ),
        [1, 1, 1],
        atol=0.001,
    )

    # compare the normal_clothing results with the figure in the standard
    assert np.allclose(
        clo_correction_factor_environment(
            vr=2,
            v_walk=[1, 0.5, 0.25],
            i_cl=[0.61, 0.71, 1.01],
        ),
        [0.503, 0.564, 0.618],
        atol=0.001,
    )

    # test that the nude function works as expected
    assert np.allclose(
        clo_correction_factor_environment(
            vr=0.15,
            v_walk=0,
            i_cl=0,
        ),
        [1],
        atol=0.001,
    )

    # compare the nude results with the figure in the standard
    assert np.allclose(
        clo_correction_factor_environment(
            vr=[0.5, 2, 3],
            v_walk=0.5,
            i_cl=0,
        ),
        [0.698, 0.394, 0.320],
        atol=0.001,
    )

    # test that the low_clothing function works as expected
    assert np.allclose(
        clo_correction_factor_environment(
            vr=0.15,
            v_walk=0,
            i_cl=[0.6, 0],
        ),
        [1, 1],
        atol=0.001,
    )


def test_transpose_sharp_altitude():
    assert transpose_sharp_altitude(sharp=0, altitude=0) == (0, 90)
    assert transpose_sharp_altitude(sharp=0, altitude=20) == (0, 70)
    assert transpose_sharp_altitude(sharp=0, altitude=45) == (0, 45)
    assert transpose_sharp_altitude(sharp=0, altitude=60) == (0, 30)
    assert transpose_sharp_altitude(sharp=90, altitude=0) == (90, 0)
    assert transpose_sharp_altitude(sharp=90, altitude=45) == (45, 0)
    assert transpose_sharp_altitude(sharp=90, altitude=30) == (60, 0)
    assert transpose_sharp_altitude(sharp=135, altitude=60) == (22.208, 20.705)
    assert transpose_sharp_altitude(sharp=120, altitude=75) == (13.064, 7.435)
    assert transpose_sharp_altitude(sharp=150, altitude=30) == (40.893, 48.590)


def test_f_svv():
    assert round(f_svv(30, 10, 3.3), 2) == 0.27
    assert round(f_svv(150, 10, 3.3), 2) == 0.31
    assert round(f_svv(30, 6, 3.3), 2) == 0.20
    assert round(f_svv(150, 6, 3.3), 2) == 0.23
    assert round(f_svv(30, 10, 6), 2) == 0.17
    assert round(f_svv(150, 10, 6), 2) == 0.21
    assert round(f_svv(30, 6, 6), 2) == 0.11
    assert round(f_svv(150, 6, 6), 2) == 0.14
    assert round(f_svv(6, 9, 3.3), 2) == 0.14
    assert round(f_svv(6, 6, 3.3), 2) == 0.11
    assert round(f_svv(6, 6, 6), 2) == 0.04
    assert round(f_svv(4, 4, 3.3), 2) == 0.06
    assert round(f_svv(4, 4, 6), 2) == 0.02


def test_running_mean_outdoor_temperature():
    assert (running_mean_outdoor_temperature([20, 20], alpha=0.7)) == 20
    assert (running_mean_outdoor_temperature([20, 20], alpha=0.9)) == 20
    assert (running_mean_outdoor_temperature([20, 20, 20, 20], alpha=0.7)) == 20
    assert (running_mean_outdoor_temperature([20, 20, 20, 20], alpha=0.5)) == 20
    assert (
        running_mean_outdoor_temperature(
            [77, 77, 77, 77, 77, 77, 77], alpha=0.8, units="IP"
        )
    ) == 77
    assert (
        running_mean_outdoor_temperature(
            [77, 77, 77, 77, 77, 77, 77], alpha=0.8, units="ip"
        )
    ) == 77


def test_ip_units_converter():
    assert (units_converter(tdb=77, tr=77, v=3.2, from_units="ip")) == [
        25.0,
        25.0,
        0.975312404754648,
    ]
    assert (units_converter(pressure=1, area=1 / 0.09, from_units="ip")) == [
        101325,
        1.0322474090590033,
    ]

    expected_result = [25.0, 3.047]
    assert np.allclose(units_converter("ip", tdb=77, v=10), expected_result, atol=0.01)

    # Test case 2: Conversion from SI to IP for temperature and velocity
    expected_result = [68, 6.562]
    assert np.allclose(units_converter("si", tdb=20, v=2), expected_result, atol=0.01)

    # Test case 3: Conversion from IP to SI for area and pressure
    expected_result = [9.29, 1489477.5]
    assert np.allclose(
        units_converter("ip", area=100, pressure=14.7), expected_result, atol=0.01
    )

    # Test case 4: Conversion from SI to IP for area and pressure
    expected_result = [538.199, 1]
    assert np.allclose(
        units_converter("si", area=50, pressure=101325), expected_result, atol=0.01
    )


def test_clo_dynamic():
    assert (clo_dynamic(clo=1, met=1, standard="ASHRAE")) == 1
    assert (clo_dynamic(clo=1, met=0.5, standard="ASHRAE")) == 1
    assert (clo_dynamic(clo=2, met=0.5, standard="ASHRAE")) == 2

    # Test ASHRAE standard
    assert np.allclose(clo_dynamic(1.0, 1.0), np.array(1))
    assert np.allclose(clo_dynamic(1.0, 1.2), np.array(1))
    assert np.allclose(clo_dynamic(1.0, 2.0), np.array(0.8))

    # Test ISO standard
    assert np.allclose(clo_dynamic(1.0, 1.0, standard="ISO"), np.array(1))
    assert np.allclose(clo_dynamic(1.0, 2.0, standard="ISO"), np.array(0.8))

    # Test invalid standard input
    with pytest.raises(ValueError):
        clo_dynamic(1.0, 1.0, standard="invalid")


def test_body_surface_area():
    assert body_surface_area(weight=80, height=1.8) == 1.9917607971689137
    assert body_surface_area(70, 1.8, "dubois") == pytest.approx(1.88, rel=1e-2)
    assert body_surface_area(75, 1.75, "takahira") == pytest.approx(1.91, rel=1e-2)
    assert body_surface_area(80, 1.7, "fujimoto") == pytest.approx(1.872, rel=1e-2)
    assert body_surface_area(85, 1.65, "kurazumi") == pytest.approx(1.89, rel=1e-2)
    with pytest.raises(ValueError):
        body_surface_area(70, 1.8, "invalid_formula")


def test_v_relative():
    # Test case when met is equal to or lower than 1
    v = 2.0
    met = 1.0
    expected_result = v
    assert np.allclose(v_relative(v, met), expected_result)

    # Test case when met is greater than 1
    v = np.array([1.0, 2.0, 3.0])
    met = 2.0
    expected_result = np.array([1.3, 2.3, 3.3])
    assert np.allclose(v_relative(v, met), expected_result, atol=1e-6)

    # Test case with negative values for v
    v = -1.5
    met = 1.5
    expected_result = -1.5 + 0.3 * 0.5
    assert np.allclose(v_relative(v, met), expected_result, atol=1e-6)
