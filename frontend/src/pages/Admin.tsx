import { Badge, Card, Loading, Note, PageTitle, useApi } from '../ui'
import { useUser } from '../App'

const PERMS: [string, boolean, boolean, boolean][] = [['View datasets, graph, comparison, provenance', true, true, true], ['Create and edit investigations', true, true, true], ['Record review decisions on edges and evidence', true, true, true], ['Export reports', true, true, true], ['View all users', false, false, true], ['Change roles', false, false, true]]
export default function Admin() {
  const u = useUser(); const { d, err, loading } = useApi<any[]>('/auth/users')
  return <div className="space-y-4"><PageTitle title="Profile and roles" sub="Account details and the role model. Accounts live in the local SQLite database data/app/orvex_app.db." />
    <div className="grid lg:grid-cols-[320px_1fr] gap-4"><Card title="Investigator profile"><div className="flex items-center gap-3"><div className="w-14 h-14 rounded-full bg-accent text-white grid place-items-center text-2xl font-bold">{(u?.name || '?')[0]}</div><div><div className="font-bold">{u?.name}</div><div className="text-[12px] text-gray-500">{u?.email}</div><Badge c="#252C5C">{u?.role}</Badge></div></div>
      <div className="mt-4"><Note>Passwords are stored as salted PBKDF2 hashes. Sessions are signed tokens that expire after 24 hours.</Note></div></Card>
      <Card title="Role and permission matrix"><table className="t"><thead><tr><th>Capability</th><th>Investigator</th><th>Reviewer</th><th>Admin</th></tr></thead><tbody>{PERMS.map(p => <tr key={p[0]}><td>{p[0]}</td>{[1, 2, 3].map(i => <td key={i}>{p[i] ? '✔' : '–'}</td>)}</tr>)}</tbody></table>
        <div className="text-[11px] text-gray-500 mt-2">In this demonstration the roles are recorded and displayed; only the user list is restricted by role.</div></Card></div>
    <Card title={u?.role === 'admin' ? 'All registered users' : 'Your account'}><Loading err={err} loading={loading} />{d && <table className="t"><thead><tr><th>Name</th><th>E-mail</th><th>Role</th><th>Created</th></tr></thead><tbody>{d.map(x => <tr key={x.email}><td>{x.name}</td><td>{x.email}</td><td><Badge>{x.role}</Badge></td><td>{x.created}</td></tr>)}</tbody></table>}</Card></div>
}
