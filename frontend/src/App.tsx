import { useEffect, useState } from 'react'
import { Activity, CircleHelp, Database, Server } from 'lucide-react'
import { getApiHealth } from './lib/api'

type HealthState = 'checking' | 'online' | 'offline'

export function App() {
  const [apiState, setApiState] = useState<HealthState>('checking')
  const [apiMessage, setApiMessage] = useState('Checking the local API…')

  useEffect(() => {
    let active = true
    getApiHealth()
      .then((health) => {
        if (!active) return
        setApiState('online')
        setApiMessage(`${health.service} is responding.`)
      })
      .catch(() => {
        if (!active) return
        setApiState('offline')
        setApiMessage('Start the backend at the configured API URL to connect.')
      })
    return () => { active = false }
  }, [])

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-12 text-slate-900 sm:px-10">
      <section className="mx-auto max-w-3xl">
        <div className="mb-10 flex items-center gap-3">
          <div className="rounded-xl bg-indigo-600 p-3 text-white"><Activity aria-hidden="true" /></div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.16em] text-indigo-700">Project foundation</p>
            <h1 className="text-3xl font-bold tracking-tight">Customer Intelligence Hub</h1>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm sm:p-9">
          <h2 className="text-xl font-semibold">Development health</h2>
          <p className="mt-2 leading-7 text-slate-600">An explainable customer intelligence framework for churn prediction and cost-aware retention prioritisation.</p>
          <div className="mt-7 grid gap-4 sm:grid-cols-2">
            <StatusCard icon={<Server />} title="Frontend" value="Ready" detail="React + TypeScript + Vite" state="online" />
            <StatusCard icon={<Activity />} title="Backend API" value={apiState === 'checking' ? 'Checking' : apiState === 'online' ? 'Connected' : 'Unavailable'} detail={apiMessage} state={apiState} />
            <StatusCard icon={<Database />} title="PostgreSQL" value="Not configured" detail="Connection settings are prepared on the backend." state="pending" />
            <StatusCard icon={<CircleHelp />} title="Next step" value="Phase 0" detail="Verify local setup before beginning implementation." state="pending" />
          </div>
          <p className="mt-7 border-t border-slate-100 pt-5 text-sm text-slate-500">This is a setup check page. Product analytics and dashboard features will be added in a later phase.</p>
        </div>
      </section>
    </main>
  )
}

function StatusCard({ icon, title, value, detail, state }: { icon: React.ReactNode; title: string; value: string; detail: string; state: HealthState | 'pending' }) {
  const color = state === 'online' ? 'bg-emerald-100 text-emerald-700' : state === 'offline' ? 'bg-rose-100 text-rose-700' : state === 'checking' ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-600'
  return (
    <div className="rounded-xl border border-slate-200 p-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-600">{title}</span>
        <span className="rounded-lg bg-slate-100 p-2 text-slate-600">{icon}</span>
      </div>
      <p className="mt-4 text-lg font-semibold">{value}</p>
      <p className={`mt-1 min-h-10 rounded-md px-2 py-1 text-sm ${color}`}>{detail}</p>
    </div>
  )
}
