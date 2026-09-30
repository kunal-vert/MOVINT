import { useCallback, useEffect, useMemo, useState, type FormEvent } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  BadgeCheck,
  CalendarDays,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  CircleHelp,
  Clock3,
  FileText,
  Filter,
  MapPin,
  Plus,
  RefreshCw,
  Search,
  ShieldAlert,
  ShieldCheck,
  UserRound,
  UsersRound,
  X,
} from "lucide-react";
import "./App.css";

const API_BASE = "http://localhost:8000/MOVINT/V2/Immigration";

type JourneyStatus = "ACTIVE" | "COMPLETED" | "OVERDUE" | "FLAGGED";

type TravelerSummary = {
  passport_id: string;
  full_name: string;
  nationality: string;
  watch_flag: boolean;
  criminal_record: boolean;
  current_journey_status: JourneyStatus | null;
  current_risk_score: number | null;
  total_journeys: number;
  entered_at: string | null;
  expected_exit_at: string | null;
};

type TravelerDetails = {
  traveler: {
    passport_id: string;
    full_name: string;
    nationality: string;
    date_of_birth: string;
    gender: string | null;
    occupation: string;
    visa_type: string;
    visa_number: string | null;
    photo_url: string | null;
    watch_flag: boolean;
    criminal_record: boolean;
    created_at: string;
  };
  journeys: Array<{
    id: string;
    status: JourneyStatus;
    current_risk_score: number;
    entered_at: string;
    exited_at: string | null;
    expected_exit_at: string;
    declared_states: string[] | null;
  }>;
  permits: Array<{
    id: string;
    type: string | null;
    issued_by: string | null;
    valid_from: string;
    valid_to: string;
    permitted_states: string[] | null;
  }>;
};

type TravelerPage = {
  total_count: number;
  pages: number;
  per_pages: number;
  travelers: TravelerSummary[];
};

const dateLabel = (value: string | null | undefined) => {
  if (!value) return "—";
  const parsed = new Date(value);
  return Number.isNaN(parsed.valueOf())
    ? "—"
    : parsed.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      });
};

const statusText = (status: JourneyStatus | null) => {
  if (!status) return "No journey";
  return status.charAt(0) + status.slice(1).toLowerCase();
};

async function readError(response: Response) {
  try {
    const body = await response.json();
    return body.detail ?? body.message ?? `Request failed (${response.status})`;
  } catch {
    return `Request failed (${response.status})`;
  }
}

function toIsoDateTime(value: FormDataEntryValue | null) {
  if (typeof value !== "string" || !value) return "";
  const date = new Date(value);
  return Number.isNaN(date.valueOf()) ? "" : date.toISOString();
}

function StatusPill({ status }: { status: JourneyStatus | null }) {
  const className = status ? `status-pill status-${status.toLowerCase()}` : "status-pill status-none";
  return <span className={className}><span className="status-dot" />{statusText(status)}</span>;
}

function App() {
  const [page, setPage] = useState<TravelerPage | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [showRegistration, setShowRegistration] = useState(false);
  const [selected, setSelected] = useState<TravelerDetails | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [formError, setFormError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const loadTravelers = useCallback(async () => {
    setLoading(true);
    setLoadError("");
    const query = new URLSearchParams({ page: "1", per_page: "100" });
    if (statusFilter !== "ALL") query.set("status", statusFilter);

    try {
      const response = await fetch(`${API_BASE}/view?${query.toString()}`);
      if (!response.ok) throw new Error(await readError(response));
      setPage((await response.json()) as TravelerPage);
    } catch (error) {
      setPage(null);
      setLoadError(
        error instanceof TypeError
          ? "Can’t reach the MOVINT API. Start the backend and check that the Immigration routes are enabled."
          : error instanceof Error
            ? error.message
            : "Could not load traveler records.",
      );
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    void loadTravelers();
  }, [loadTravelers]);

  const travelers = useMemo(() => {
    const needle = search.trim().toLowerCase();
    return (page?.travelers ?? []).filter((traveler) =>
      !needle ||
      traveler.full_name.toLowerCase().includes(needle) ||
      traveler.passport_id.toLowerCase().includes(needle) ||
      traveler.nationality.toLowerCase().includes(needle),
    );
  }, [page, search]);

  const activeCount = (page?.travelers ?? []).filter(
    (traveler) => traveler.current_journey_status === "ACTIVE",
  ).length;
  const watchCount = (page?.travelers ?? []).filter((traveler) => traveler.watch_flag).length;
  const flaggedCount = (page?.travelers ?? []).filter(
    (traveler) => traveler.current_journey_status === "FLAGGED" || traveler.current_journey_status === "OVERDUE",
  ).length;

  const openTraveler = async (passportId: string) => {
    setSelected(null);
    setDetailLoading(true);
    try {
      const response = await fetch(`${API_BASE}/view/${encodeURIComponent(passportId)}`);
      if (!response.ok) throw new Error(await readError(response));
      setSelected((await response.json()) as TravelerDetails);
    } catch (error) {
      setLoadError(error instanceof Error ? error.message : "Could not open traveler record.");
    } finally {
      setDetailLoading(false);
    }
  };

  const submitRegistration = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError("");
    setSuccessMessage("");
    const form = event.currentTarget;
    const data = new FormData(form);
    const expectedExit = toIsoDateTime(data.get("expected_exit_at"));
    const permitFrom = toIsoDateTime(data.get("permit_valid_from"));
    const permitTo = toIsoDateTime(data.get("permit_valid_to"));

    if (!expectedExit || !permitFrom || !permitTo) {
      setFormError("Enter valid dates for the expected exit and permit validity.");
      return;
    }

    const splitStates = (value: FormDataEntryValue | null) =>
      typeof value === "string" && value.trim()
        ? value.split(",").map((state) => state.trim()).filter(Boolean)
        : null;

    const payload = {
      passport_id: data.get("passport_id"),
      nationality: data.get("nationality"),
      full_name: data.get("full_name"),
      date_of_birth: data.get("date_of_birth"),
      gender: data.get("gender"),
      photo_url: data.get("photo_url") || null,
      criminal_record: data.get("criminal_record") === "on",
      entry_checkpoint_id: data.get("entry_checkpoint_id"),
      occupation: data.get("occupation"),
      visa_type: data.get("visa_type"),
      visa_number: data.get("visa_number") || null,
      permit_type: data.get("permit_type") || null,
      permit_issued_by: data.get("permit_issued_by") || null,
      permit_valid_from: permitFrom,
      permit_valid_to: permitTo,
      permit_permitted_states: splitStates(data.get("permit_permitted_states")),
      declared_states: splitStates(data.get("declared_states")),
      expected_exit_at: expectedExit,
    };

    setSubmitting(true);
    try {
      const response = await fetch(`${API_BASE}/reg`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error(await readError(response));
      const result = await response.json();
      setSuccessMessage(result.message ?? "Traveler registered successfully.");
      setShowRegistration(false);
      form.reset();
      await loadTravelers();
    } catch (error) {
      setFormError(
        error instanceof TypeError
          ? "Can’t reach the MOVINT API. Check that the backend is running and its Immigration routes are enabled."
          : error instanceof Error
            ? error.message
            : "Registration could not be completed.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="movint-app">
      <aside className="sidebar">
        <a className="brand" href="#top" aria-label="MOVINT home">
          <span className="brand-mark"><Activity size={20} strokeWidth={2.4} /></span>
          <span className="brand-copy"><strong>MOVINT</strong><small>FIELD INTELLIGENCE</small></span>
        </a>

        <div className="sidebar-label">WORKSPACE</div>
        <nav className="side-nav" aria-label="Main navigation">
          <a className="nav-item active" href="#registry"><UsersRound size={17} />Traveler registry</a>
          <a className="nav-item" href="#registry"><MapPin size={17} />Movement overview</a>
          <a className="nav-item" href="#registry"><ShieldCheck size={17} />Watch list</a>
        </nav>

        <div className="sidebar-bottom">
          <div className="support-card">
            <span className="support-icon"><CircleHelp size={17} /></span>
            <strong>Need a hand?</strong>
            <span>Contact your system administrator for access support.</span>
          </div>
          <div className="operator-row">
            <div className="operator-avatar">MO</div>
            <div className="operator-copy"><strong>Movement office</strong><span>Regional operations</span></div>
            <ChevronDown size={16} className="operator-chevron" />
          </div>
        </div>
      </aside>

      <main className="main-content" id="top">
        <header className="topbar">
          <div className="breadcrumb"><span>Workspace</span><ChevronRight size={14} /><strong>Traveler registry</strong></div>
          <div className="topbar-right">
            <span className="environment-pill"><span />REGIONAL OPERATIONS</span>
            <span className="topbar-divider" />
            <span className="date-stamp"><CalendarDays size={15} />{new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" })}</span>
          </div>
        </header>

        <div className="page-wrap" id="registry">
          <section className="page-heading">
            <div>
              <div className="eyebrow"><span className="eyebrow-line" />MOVEMENT INTELLIGENCE</div>
              <h1>Traveler registry</h1>
              <p>Review entry records, monitor active journeys, and register incoming travelers.</p>
            </div>
            <div className="heading-actions">
              <button className="button button-light" onClick={() => void loadTravelers()} disabled={loading}>
                <RefreshCw size={16} className={loading ? "spin" : ""} />Refresh
              </button>
              <button className="button button-primary" onClick={() => { setFormError(""); setShowRegistration(true); }}>
                <Plus size={17} />Register traveler
              </button>
            </div>
          </section>

          {successMessage && <div className="success-banner"><BadgeCheck size={18} /><span>{successMessage}</span><button onClick={() => setSuccessMessage("")} aria-label="Dismiss"><X size={16} /></button></div>}

          <section className="stats-grid" aria-label="Traveler registry summary">
            <article className="stat-card">
              <div className="stat-top"><span className="stat-icon stat-icon-blue"><UsersRound size={18} /></span><span className="stat-kicker">RECORDS</span></div>
              <div className="stat-value">{loading ? "—" : page?.total_count ?? "—"}</div>
              <div className="stat-foot"><span>Total registered</span><span className="stat-trend"><ArrowUpRight size={14} />All records</span></div>
            </article>
            <article className="stat-card">
              <div className="stat-top"><span className="stat-icon stat-icon-green"><MapPin size={18} /></span><span className="stat-kicker">JOURNEYS</span></div>
              <div className="stat-value">{loading ? "—" : activeCount}</div>
              <div className="stat-foot"><span>Active in loaded records</span><span className="stat-trend">In progress</span></div>
            </article>
            <article className="stat-card">
              <div className="stat-top"><span className="stat-icon stat-icon-amber"><ShieldAlert size={18} /></span><span className="stat-kicker">ATTENTION</span></div>
              <div className="stat-value">{loading ? "—" : flaggedCount}</div>
              <div className="stat-foot"><span>Overdue or flagged</span><span className="stat-trend stat-trend-warn"><AlertTriangle size={14} />Review</span></div>
            </article>
            <article className="stat-card">
              <div className="stat-top"><span className="stat-icon stat-icon-violet"><ShieldCheck size={18} /></span><span className="stat-kicker">WATCH LIST</span></div>
              <div className="stat-value">{loading ? "—" : watchCount}</div>
              <div className="stat-foot"><span>Watch-listed travelers</span><span className="stat-trend">Monitored</span></div>
            </article>
          </section>

          <section className="registry-card">
            <div className="registry-header">
              <div><h2>Tracked travelers</h2><p>Search traveler records and review current journey status.</p></div>
              <span className="record-count">{page?.total_count ?? 0} RECORDS</span>
            </div>

            <div className="table-toolbar">
              <label className="search-box"><Search size={17} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search name, passport, or nationality" /></label>
              <label className="filter-select"><Filter size={16} /><select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}><option value="ALL">All journeys</option><option value="ACTIVE">Active</option><option value="COMPLETED">Completed</option><option value="OVERDUE">Overdue</option><option value="FLAGGED">Flagged</option></select><ChevronDown size={15} /></label>
            </div>

            {loadError && <div className="error-banner"><AlertTriangle size={18} /><span>{loadError}</span><button onClick={() => void loadTravelers()}>Retry</button></div>}

            <div className="table-scroll">
              <table>
                <thead><tr><th>TRAVELER</th><th>PASSPORT ID</th><th>JOURNEY STATUS</th><th>RISK</th><th>ENTRY DATE</th><th>EXPECTED EXIT</th><th aria-label="Actions" /></tr></thead>
                <tbody>
                  {loading ? <tr><td colSpan={7} className="table-message"><RefreshCw size={16} className="spin" />Loading traveler records…</td></tr> : travelers.length ? travelers.map((traveler) => (
                    <tr key={traveler.passport_id} className="traveler-row" onClick={() => void openTraveler(traveler.passport_id)}>
                      <td><div className="traveler-cell"><span className="traveler-avatar">{traveler.full_name.split(/\s+/).slice(0, 2).map((part) => part[0]).join("").toUpperCase()}</span><span><strong>{traveler.full_name}</strong><small>{traveler.nationality}{traveler.watch_flag && <span className="mini-flag">WATCH</span>}</small></span></div></td>
                      <td><span className="passport-code">{traveler.passport_id}</span></td>
                      <td><StatusPill status={traveler.current_journey_status} /></td>
                      <td><span className={`risk-score ${Number(traveler.current_risk_score ?? 0) >= 70 ? "risk-high" : Number(traveler.current_risk_score ?? 0) >= 40 ? "risk-medium" : "risk-low"}`}>{traveler.current_risk_score ?? "—"}<small>/100</small></span></td>
                      <td><span className="table-date">{dateLabel(traveler.entered_at)}</span></td>
                      <td><span className="table-date">{dateLabel(traveler.expected_exit_at)}</span></td>
                      <td><button className="row-open" aria-label={`Open ${traveler.full_name}`} onClick={(event) => { event.stopPropagation(); void openTraveler(traveler.passport_id); }}><ChevronRight size={17} /></button></td>
                    </tr>
                  )) : <tr><td colSpan={7} className="empty-state"><span className="empty-icon"><Search size={19} /></span><strong>{loadError ? "Records are unavailable" : "No matching travelers"}</strong><span>{loadError ? "Connect to the API to see the registry." : "Try a different search or register a traveler."}</span></td></tr>}
                </tbody>
              </table>
            </div>

            <div className="table-footer">
              <span>Showing <strong>{travelers.length}</strong> of <strong>{page?.total_count ?? 0}</strong> records</span>
              <div className="pagination"><button disabled aria-label="Previous page"><ChevronLeft size={16} /></button><span>1</span><button disabled aria-label="Next page"><ChevronRight size={16} /></button></div>
            </div>
          </section>

          <footer className="page-footer"><span><ShieldCheck size={14} />Secure movement records</span><span>© {new Date().getFullYear()} MOVINT <i /> Regional operations</span></footer>
        </div>
      </main>

      {showRegistration && <div className="overlay" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setShowRegistration(false); }}>
        <section className="registration-panel" role="dialog" aria-modal="true" aria-labelledby="registration-title">
          <div className="panel-header"><div><span className="panel-eyebrow">ENTRY CHECKPOINT</span><h2 id="registration-title">Register traveler</h2><p>Create a traveler record and open a new journey.</p></div><button className="icon-button" onClick={() => setShowRegistration(false)} aria-label="Close registration"><X size={19} /></button></div>
          {formError && <div className="error-banner form-error"><AlertTriangle size={18} /><span>{formError}</span></div>}
          <form onSubmit={submitRegistration} className="registration-form">
            <div className="form-section-title"><span>01</span><div><strong>Identity details</strong><small>Use the information shown on the travel document.</small></div></div>
            <div className="form-grid">
              <label className="form-field"><span>Full name <b>*</b></span><input name="full_name" required minLength={2} maxLength={50} placeholder="As shown on passport" /></label>
              <label className="form-field"><span>Passport ID <b>*</b></span><input name="passport_id" required minLength={7} maxLength={50} placeholder="e.g. GBP-874221X" /></label>
              <label className="form-field"><span>Nationality <b>*</b></span><input name="nationality" required minLength={2} maxLength={30} placeholder="Country of citizenship" /></label>
              <label className="form-field"><span>Date of birth <b>*</b></span><input name="date_of_birth" required type="date" /></label>
              <label className="form-field"><span>Gender</span><select name="gender" defaultValue="unknown"><option value="unknown">Prefer not to say</option><option value="female">Female</option><option value="male">Male</option><option value="other">Other</option></select></label>
              <label className="form-field"><span>Occupation <b>*</b></span><input name="occupation" required minLength={2} maxLength={50} placeholder="Declared occupation" /></label>
              <label className="form-field"><span>Photo URL</span><input name="photo_url" type="url" placeholder="https://…" /></label>
              <label className="check-field"><input name="criminal_record" type="checkbox" /><span>Criminal record declared or verified</span></label>
            </div>

            <div className="form-section-title form-section-next"><span>02</span><div><strong>Entry and visa</strong><small>Journey and permit details for this visit.</small></div></div>
            <div className="form-grid">
              <label className="form-field full-field"><span>Entry checkpoint ID <b>*</b></span><input name="entry_checkpoint_id" required placeholder="Paste the checkpoint UUID" /></label>
              <label className="form-field"><span>Visa type <b>*</b></span><input name="visa_type" required minLength={2} maxLength={100} placeholder="Tourist / Research / Business" /></label>
              <label className="form-field"><span>Visa number</span><input name="visa_number" maxLength={100} placeholder="Document number" /></label>
              <label className="form-field"><span>Permit type</span><select name="permit_type" defaultValue=""><option value="">Select permit</option><option value="ILP">ILP</option><option value="RAP">RAP</option><option value="TOURIST_VISA">Tourist visa</option><option value="RESEARCH_PERMIT">Research permit</option></select></label>
              <label className="form-field"><span>Issued by</span><input name="permit_issued_by" maxLength={255} placeholder="Issuing authority" /></label>
              <label className="form-field"><span>Permit valid from <b>*</b></span><input name="permit_valid_from" required type="datetime-local" /></label>
              <label className="form-field"><span>Permit valid to <b>*</b></span><input name="permit_valid_to" required type="datetime-local" /></label>
              <label className="form-field"><span>Expected exit <b>*</b></span><input name="expected_exit_at" required type="datetime-local" /></label>
              <label className="form-field"><span>Declared states</span><input name="declared_states" placeholder="Comma-separated state names" /></label>
              <label className="form-field full-field"><span>Permit permitted states</span><input name="permit_permitted_states" placeholder="Comma-separated permitted states" /></label>
            </div>
            <div className="form-actions"><button type="button" className="button button-light" onClick={() => setShowRegistration(false)}>Cancel</button><button className="button button-primary" type="submit" disabled={submitting}>{submitting ? <><RefreshCw size={15} className="spin" />Saving…</> : <><Plus size={16} />Register traveler</>}</button></div>
          </form>
        </section>
      </div>}

      {(selected || detailLoading) && <div className="overlay detail-overlay" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setSelected(null); }}>
        <section className="detail-panel" role="dialog" aria-modal="true" aria-labelledby="detail-title">
          <div className="detail-top"><span className="detail-eyebrow">TRAVELER RECORD</span><button className="icon-button" onClick={() => setSelected(null)} aria-label="Close traveler details"><X size={19} /></button></div>
          {detailLoading ? <div className="detail-loading"><RefreshCw size={19} className="spin" />Loading record…</div> : selected && <>
            <div className="detail-person"><span className="detail-avatar">{selected.traveler.full_name.split(/\s+/).slice(0, 2).map((part) => part[0]).join("").toUpperCase()}</span><div><h2 id="detail-title">{selected.traveler.full_name}</h2><p>{selected.traveler.nationality} <span>·</span> {selected.traveler.passport_id}</p></div></div>
            <div className="detail-badges">{selected.traveler.watch_flag && <span className="mini-flag">WATCH LIST</span>}{selected.traveler.criminal_record && <span className="detail-warning"><AlertTriangle size={13} />Declared record</span>}</div>
            <div className="detail-block"><div className="detail-block-heading"><UserRound size={16} /><strong>Personal details</strong></div><div className="detail-facts"><span>Date of birth</span><strong>{dateLabel(selected.traveler.date_of_birth)}</strong><span>Gender</span><strong>{selected.traveler.gender ?? "—"}</strong><span>Occupation</span><strong>{selected.traveler.occupation}</strong><span>Visa</span><strong>{selected.traveler.visa_type}{selected.traveler.visa_number ? ` · ${selected.traveler.visa_number}` : ""}</strong></div></div>
            <div className="detail-block"><div className="detail-block-heading"><Clock3 size={16} /><strong>Journey history</strong><span>{selected.journeys.length}</span></div>{selected.journeys.length ? selected.journeys.map((journey) => <div className="history-row" key={journey.id}><span className="history-marker" /><div className="history-copy"><strong>{statusText(journey.status)} journey</strong><small>{dateLabel(journey.entered_at)} · Expected exit {dateLabel(journey.expected_exit_at)}</small></div><span className="history-risk">Risk {journey.current_risk_score}</span></div>) : <p className="detail-empty">No journeys recorded.</p>}</div>
            <div className="detail-block"><div className="detail-block-heading"><FileText size={16} /><strong>Permits</strong><span>{selected.permits.length}</span></div>{selected.permits.length ? selected.permits.map((permit) => <div className="permit-row" key={permit.id}><div><strong>{permit.type ?? "Travel permit"}</strong><small>{permit.issued_by ?? "Issuing authority not listed"}</small></div><span>{dateLabel(permit.valid_from)} – {dateLabel(permit.valid_to)}</span></div>) : <p className="detail-empty">No permits recorded.</p>}</div>
          </>}
        </section>
      </div>}
    </div>
  );
}

export default App;
