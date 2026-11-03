#!/bin/bash

systemctl daemon-reload
systemctl enable dato38itbot.service
systemctl start dato38itbot.service
systemctl status dato38itbot.service