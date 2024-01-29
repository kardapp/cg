"""Test fixtures for cg/server tests"""
import os
from datetime import datetime
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from mock import patch

from cg.constants import DataDelivery, Pipeline
from cg.server.ext import db as store
from cg.store.database import create_all_tables, drop_all_tables
from cg.store.models import Case, Order
from tests.store_helpers import StoreHelpers

os.environ["CG_SQL_DATABASE_URI"] = "sqlite:///"
os.environ["LIMS_HOST"] = "dummy_value"
os.environ["LIMS_USERNAME"] = "dummy_value"
os.environ["LIMS_PASSWORD"] = "dummy_value"
os.environ["GOOGLE_OAUTH_CLIENT_ID"] = "dummy_value"
os.environ["GOOGLE_OAUTH_CLIENT_SECRET"] = "dummy_value"
os.environ["CG_ENABLE_ADMIN"] = "1"


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    from cg.server.auto import app

    app.config.update({"TESTING": True})
    create_all_tables()
    yield app
    drop_all_tables()


@pytest.fixture
def case(helpers: StoreHelpers) -> Case:
    case: Case = helpers.add_case(
        customer_id=1,
        data_analysis=Pipeline.MIP_DNA,
        data_delivery=DataDelivery.ANALYSIS_SCOUT,
        name="test case",
        ticket="123",
        store=store,
    )
    return case


@pytest.fixture
def order(helpers: StoreHelpers) -> Order:
    order: Order = helpers.add_order(
        store=store, customer_id=1, ticket_id=1, order_date=datetime.now()
    )
    return order


@pytest.fixture
def order_another(helpers: StoreHelpers) -> Order:
    order: Order = helpers.add_order(
        store=store, customer_id=2, ticket_id=2, order_date=datetime.now()
    )
    return order


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    # Bypass authentication
    with patch.object(app, "before_request_funcs", new={}):
        yield app.test_client()
