"""Testovi za vizualne efekte: flash overlay i čestice eksplozija."""

import pytest

from aetherfront.rendering.effects import (
    EffectsState,
    ExplosionParticle,
    spawn_explosion,
    update_particles,
)


class TestSpawnExplosion:
    def test_returns_correct_count(self):
        particles = spawn_explosion(100.0, 200.0, count=8)
        assert len(particles) == 8

    def test_default_count(self):
        particles = spawn_explosion(0.0, 0.0)
        assert len(particles) == 10

    def test_particles_start_at_origin(self):
        particles = spawn_explosion(50.0, 75.0)
        for p in particles:
            assert p.x == pytest.approx(50.0)
            assert p.y == pytest.approx(75.0)

    def test_particles_are_active(self):
        particles = spawn_explosion(0.0, 0.0)
        assert all(p.active for p in particles)

    def test_particles_have_positive_lifetime(self):
        particles = spawn_explosion(0.0, 0.0)
        assert all(p.lifetime > 0.0 for p in particles)

    def test_particles_have_nonzero_velocity(self):
        particles = spawn_explosion(0.0, 0.0)
        assert all(abs(p.vx) > 0.0 or abs(p.vy) > 0.0 for p in particles)


class TestExplosionParticle:
    def _make(self, lifetime: float = 1.0) -> ExplosionParticle:
        return ExplosionParticle(
            x=0.0, y=0.0, vx=10.0, vy=0.0,
            size=3.0, lifetime=lifetime, lifetime_remaining=lifetime,
        )

    def test_active_when_lifetime_positive(self):
        p = self._make(1.0)
        assert p.active

    def test_inactive_when_lifetime_zero(self):
        p = self._make(0.0)
        assert not p.active

    def test_update_moves_particle(self):
        p = self._make(1.0)
        p.update(0.1)
        assert p.x == pytest.approx(1.0)

    def test_update_decrements_lifetime(self):
        p = self._make(1.0)
        p.update(0.5)
        assert p.lifetime_remaining == pytest.approx(0.5)

    def test_update_expires_particle(self):
        p = self._make(0.1)
        p.update(0.2)
        assert not p.active


class TestUpdateParticles:
    def test_removes_expired(self):
        particles = [
            ExplosionParticle(0, 0, 0, 0, 3.0, 1.0, 0.05),
            ExplosionParticle(0, 0, 0, 0, 3.0, 1.0, 1.0),
        ]
        result = update_particles(particles, 0.1)
        assert len(result) == 1

    def test_empty_list(self):
        assert update_particles([], 0.1) == []


class TestEffectsState:
    def test_initial_state(self):
        e = EffectsState()
        assert e.flash_alpha == 0.0
        assert e.flash_remaining == 0.0
        assert e.particles == []

    def test_trigger_flash(self):
        e = EffectsState()
        e.trigger_flash(100.0, 0.5)
        assert e.flash_alpha == pytest.approx(100.0)
        assert e.flash_remaining == pytest.approx(0.5)

    def test_trigger_flash_keeps_max(self):
        e = EffectsState()
        e.trigger_flash(50.0, 0.3)
        e.trigger_flash(80.0, 0.1)
        assert e.flash_alpha == pytest.approx(80.0)
        assert e.flash_remaining == pytest.approx(0.3)

    def test_flash_expires_after_update(self):
        e = EffectsState()
        e.trigger_flash(100.0, 0.1)
        e.update(0.2)
        assert e.flash_alpha == 0.0
        assert e.flash_remaining == 0.0

    def test_add_explosion_adds_particles(self):
        e = EffectsState()
        e.add_explosion(10.0, 20.0)
        assert len(e.particles) == 10

    def test_update_removes_expired_particles(self):
        e = EffectsState()
        e.add_explosion(0.0, 0.0)
        e.update(10.0)
        assert e.particles == []
