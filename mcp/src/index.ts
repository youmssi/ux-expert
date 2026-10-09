#!/usr/bin/env node
import { serveStdio } from '@modelcontextprotocol/server/stdio';

import { createServer } from './server.js';
import { findSkillDir } from './skill.js';

const skillDir = findSkillDir();
void serveStdio(() => createServer(skillDir));
// stdout carries the protocol; diagnostics go to stderr.
console.error(`ux-expert MCP server running on stdio (skill: ${skillDir})`);
