# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from flask.ext.login import login_required
from itertools import chain
import boto.ec2
from sgannotate.security.models import Annotation

blueprint = Blueprint("security", __name__, url_prefix='/security',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def show():
    annotations = {a.cidr: a.name for a in Annotation.query.all()}
    conn = boto.ec2.connect_to_region("eu-west-1")
    aws_sgs = conn.get_all_security_groups()
    security_groups = []
    for sg in aws_sgs:
        security_groups.append(_convert_group(sg, annotations))

    return render_template("security/show.html", security_groups=sorted(security_groups, key=lambda s: s['name']))


@blueprint.route("/annotate", methods=["POST"])
def annotate():
    print request.form['pk']
    Annotation.upsert(cidr=request.form['pk'], name=request.form['value'])
    return "ok", 200


def _convert_group(aws_sg, annotations):
    grants = []
    for rule in aws_sg.rules:
        grants.extend([{'cidr': cidr, 'proto': _protocol_repr(rule), 'name': annotations.get(unicode(cidr), '')}
                       for cidr in rule.grants])
    instances = "<br/>".join([i.tags['Name'] for i in aws_sg.instances()])
    return {
        'id': aws_sg.id,
        'name': aws_sg.name,
        'grants': grants,
        'instances': instances if instances else "None"
    }

def _protocol_repr(rule):
    proto = "all" if rule.ip_protocol == "-1" else rule.ip_protocol
    from_port = "0" if not rule.from_port else rule.from_port
    to_port = "65535" if not rule.to_port else rule.to_port
    port_range = from_port if from_port == to_port else "{}-{}".format(from_port, to_port)
    return "{}({})".format(proto, port_range)
