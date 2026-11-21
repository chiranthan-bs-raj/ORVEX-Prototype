import { LayoutDashboard, FolderSearch, Users, Network, GitCompare, GitBranch, Wand2, Share2, FileSearch, Database, Layers, ShieldCheck, Cpu, BarChart3, FileText, Settings } from 'lucide-react'

/** Sidebar structure. Routes and page names are the existing ones; only the group names are investigation-themed. */
export const NAV: [string, [string, string, any][]][] = [
  ['Command centre', [['/', 'Dashboard', LayoutDashboard], ['/investigations', 'Investigations', FolderSearch]]],
  ['Media investigation', [['/candidates', 'Candidate discovery', Users], ['/graph', 'Relationship graph', Network], ['/compare', 'Video comparison', GitCompare], ['/provenance', 'Media provenance', GitBranch]]],
  ['Forensic analysis', [['/manipulation', 'Manipulation analysis', Wand2], ['/distribution', 'Distribution and campaigns', Share2]]],
  ['Evidence management', [['/evidence', 'Evidence ledger', FileSearch]]],
  ['Data intelligence', [['/datasets', 'Dataset explorer', Database], ['/variants', 'Variants and labels', Layers], ['/quality', 'Data quality', ShieldCheck]]],
  ['Models and evaluation', [['/models', 'Model lab', Cpu], ['/evaluation', 'Evaluation', BarChart3]]],
  ['Reports', [['/report', 'Investigation report', FileText]]],
  ['Administration', [['/admin', 'Profile and roles', Settings]]]]
export const TITLES: Record<string, string> = Object.fromEntries(NAV.flatMap(([, l]) => l.map(([p, n]) => [p, n])))
export const SECTION: Record<string, string> = Object.fromEntries(NAV.flatMap(([g, l]) => l.map(([p]) => [p, g])))
