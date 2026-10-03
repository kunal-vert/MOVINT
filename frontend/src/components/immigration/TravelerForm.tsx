import { useState, type FormEvent, type InputHTMLAttributes } from 'react'
import { AlertTriangle, ArrowLeft, BadgeCheck, Plane, ShieldCheck } from 'lucide-react'
import { Link } from 'react-router-dom'
import DateField, { DateTimeField } from './DateField'
import { Badge } from '@/components/shadcn/badge'
import { Button } from '@/components/shadcn/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/shadcn/card'
import { Checkbox } from '@/components/shadcn/checkbox'
import { Input } from '@/components/shadcn/input'
import { Label } from '@/components/shadcn/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/shadcn/select'
import { Separator } from '@/components/shadcn/separator'
import { Textarea } from '@/components/shadcn/textarea'

type FormValues = {
  passportId: string
  nationality: string
  fullName: string
  dateOfBirth: string
  gender: string
  photoUrl: string
  criminalRecord: boolean
  entryCheckpointId: string
  occupation: string
  visaType: string
  visaNumber: string
  permitType: string
  permitIssuedBy: string
  permitValidFromDate: string
  permitValidFromTime: string
  permitValidToDate: string
  permitValidToTime: string
  permitPermittedStates: string
  declaredStates: string
  expectedExitDate: string
  expectedExitTime: string
}

const initialValues: FormValues = {
  passportId: '',
  nationality: '',
  fullName: '',
  dateOfBirth: '',
  gender: 'unknown',
  photoUrl: '',
  criminalRecord: false,
  entryCheckpointId: '',
  occupation: '',
  visaType: '',
  visaNumber: '',
  permitType: '',
  permitIssuedBy: '',
  permitValidFromDate: '',
  permitValidFromTime: '',
  permitValidToDate: '',
  permitValidToTime: '',
  permitPermittedStates: '',
  declaredStates: '',
  expectedExitDate: '',
  expectedExitTime: '',
}

interface TextFieldProps {
  id: string
  label: string
  value: string
  onChange: (value: string) => void
  type?: InputHTMLAttributes<HTMLInputElement>['type']
  placeholder?: string
  minLength?: number
  maxLength?: number
  required?: boolean
  helper?: string
}

function TextField({
  id,
  label,
  value,
  onChange,
  type = 'text',
  placeholder,
  minLength,
  maxLength,
  required = false,
  helper,
}: TextFieldProps) {
  return (
    <div className="grid content-start gap-2">
      <Label htmlFor={id} className="text-sm text-white/80">
        {label}{required ? ' *' : ''}
      </Label>
      <Input
        id={id}
        type={type}
        value={value}
        placeholder={placeholder}
        minLength={minLength}
        maxLength={maxLength}
        required={required}
        onChange={(event) => onChange(event.target.value)}
        className="h-10 border-white/10 bg-black/35 text-white placeholder:text-white/30 [color-scheme:dark]"
      />
      {helper && <p className="text-xs leading-relaxed text-white/45">{helper}</p>}
    </div>
  )
}

function splitStates(value: string) {
  const states = value
    .split(/[\n,]/)
    .map((state) => state.trim())
    .filter(Boolean)
  return states.length ? states : null
}

function toIsoDateTime(date: string, time: string) {
  const [year, month, day] = date.split('-').map(Number)
  const [hours, minutes] = time.split(':').map(Number)
  return new Date(year, month - 1, day, hours, minutes).toISOString()
}

function localDateTime(date: string, time: string) {
  if (!date || !time) return null
  const [year, month, day] = date.split('-').map(Number)
  const [hours, minutes] = time.split(':').map(Number)
  return new Date(year, month - 1, day, hours, minutes)
}

function formatApiError(payload: unknown) {
  if (typeof payload === 'object' && payload !== null && 'detail' in payload) {
    const detail = payload.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) {
      return detail
        .map((issue) => {
          if (typeof issue !== 'object' || issue === null) return String(issue)
          const field = Array.isArray(issue.loc) ? issue.loc.slice(1).join('.') : ''
          return `${field ? `${field}: ` : ''}${String(issue.msg ?? 'Invalid value')}`
        })
        .join(' ')
    }
  }
  return 'Registration could not be completed. Check the details and try again.'
}

export default function TravelerForm() {
  const [form, setForm] = useState<FormValues>(initialValues)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const update = <K extends keyof FormValues>(key: K, value: FormValues[K]) => {
    setForm((current) => ({ ...current, [key]: value }))
    setError('')
    setSuccess('')
  }

  const today = new Date()
  const latestAdultBirthDate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate())

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setSuccess('')

    const checkpointId = form.entryCheckpointId.trim()
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(checkpointId)) {
      setError('Enter a valid UUID for the active Airport entry checkpoint.')
      return
    }

    const birthDate = form.dateOfBirth ? new Date(`${form.dateOfBirth}T12:00:00`) : null
    if (!birthDate || birthDate > latestAdultBirthDate) {
      setError('Traveler must be at least 18 years old.')
      return
    }

    const validFrom = localDateTime(form.permitValidFromDate, form.permitValidFromTime)
    const validTo = localDateTime(form.permitValidToDate, form.permitValidToTime)
    const expectedExit = localDateTime(form.expectedExitDate, form.expectedExitTime)
    if (!validFrom || !validTo || !expectedExit) {
      setError('Complete all permit and expected exit date and time fields.')
      return
    }
    if (validTo <= validFrom) {
      setError('Permit valid-to must be after permit valid-from.')
      return
    }
    if (expectedExit <= new Date()) {
      setError('Expected exit must be in the future.')
      return
    }

    const payload = {
      passport_id: form.passportId.trim().toUpperCase(),
      nationality: form.nationality.trim(),
      full_name: form.fullName.trim(),
      date_of_birth: form.dateOfBirth,
      gender: form.gender || 'unknown',
      photo_url: form.photoUrl.trim() || null,
      criminal_record: form.criminalRecord,
      entry_checkpoint_id: checkpointId,
      occupation: form.occupation.trim(),
      visa_type: form.visaType.trim(),
      visa_number: form.visaNumber.trim() || null,
      permit_type: form.permitType.trim() || null,
      permit_issued_by: form.permitIssuedBy.trim() || null,
      permit_valid_from: toIsoDateTime(form.permitValidFromDate, form.permitValidFromTime),
      permit_valid_to: toIsoDateTime(form.permitValidToDate, form.permitValidToTime),
      permit_permitted_states: splitStates(form.permitPermittedStates),
      declared_states: splitStates(form.declaredStates),
      expected_exit_at: toIsoDateTime(form.expectedExitDate, form.expectedExitTime),
    }

    const configuredApiBase = import.meta.env.VITE_API_BASE_URL
    const apiBase = configuredApiBase || (import.meta.env.DEV ? '/api' : '')
    const registrationUrl = `${apiBase.replace(/\/$/, '')}/MOVINT/V2/Immigration/reg`

    setSubmitting(true)
    try {
      const response = await fetch(registrationUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      const responseBody: unknown = await response.json().catch(() => null)
      if (!response.ok) {
        setError(formatApiError(responseBody))
        return
      }

      const message =
        typeof responseBody === 'object' && responseBody !== null && 'message' in responseBody
          ? String(responseBody.message)
          : 'Traveler registered successfully.'
      setSuccess(message)
      setForm(initialValues)
    } catch {
      setError('Could not connect to the registration service. Confirm the backend is running and try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="w-full flex-1 px-2 pb-12 pt-7 max-[600px]:px-0 max-[600px]:pt-5">
      <div className="mx-auto w-full max-w-6xl">
        <div className="mb-6 flex items-center justify-between gap-4 max-[600px]:items-start">
          <div>
            <Link
              to="/deployment"
              className="mb-4 inline-flex items-center gap-2 text-xs font-medium tracking-[0.12em] text-white/55 no-underline transition-colors hover:text-cyan-100"
            >
              <ArrowLeft className="size-3.5" /> DEPLOYMENT
            </Link>
            <div className="flex items-center gap-3">
              <span className="grid size-11 place-items-center rounded-xl border border-cyan-200/15 bg-cyan-100/[0.06] text-cyan-100">
                <Plane className="size-5" />
              </span>
              <div>
                <p className="mb-1 text-[10px] font-semibold tracking-[0.2em] text-cyan-100/60">AIRPORT IMMIGRATION</p>
                <h1 className="text-2xl font-semibold tracking-[0.03em] text-white max-[600px]:text-xl">
                  Traveler registration
                </h1>
              </div>
            </div>
          </div>
          <Badge className="mt-9 border border-white/10 bg-white/[0.04] text-[10px] tracking-[0.12em] text-white/55 max-[600px]:hidden">
            <ShieldCheck data-icon="inline-start" /> SECURE INTAKE
          </Badge>
        </div>

        <Card className="border-white/10 bg-[#0b1014]/95 text-white shadow-[0_24px_80px_rgba(0,0,0,0.35)]">
          <CardHeader className="gap-2 border-b border-white/[0.07] px-6 py-5 max-[600px]:px-4">
            <CardTitle className="text-lg tracking-wide text-white">Registration record</CardTitle>
            <CardDescription className="max-w-3xl text-sm leading-relaxed text-white/50">
              Enter the traveler, permit, and journey details required to open an active airport journey. Required fields are marked with *.
            </CardDescription>
          </CardHeader>

          <CardContent className="px-6 py-6 max-[600px]:px-4">
            <form className="grid gap-8" onSubmit={handleSubmit}>
              <section className="grid gap-4" aria-labelledby="traveler-section-title">
                <SectionHeading id="traveler-section-title" title="Traveler details" description="Identity information as recorded on travel documents." />
                <div className="grid grid-cols-2 gap-x-5 gap-y-5 max-[700px]:grid-cols-1">
                  <TextField
                    id="full-name"
                    label="Full name"
                    value={form.fullName}
                    onChange={(value) => update('fullName', value)}
                    minLength={2}
                    maxLength={50}
                    required
                    placeholder="Name as shown on passport"
                  />
                  <TextField
                    id="passport-id"
                    label="Passport ID"
                    value={form.passportId}
                    onChange={(value) => update('passportId', value)}
                    minLength={7}
                    maxLength={50}
                    required
                    placeholder="GBP-874221X"
                    helper="Will be normalized to uppercase."
                  />
                  <TextField
                    id="nationality"
                    label="Nationality"
                    value={form.nationality}
                    onChange={(value) => update('nationality', value)}
                    minLength={2}
                    maxLength={30}
                    required
                    placeholder="Country of citizenship"
                  />
                  <div className="grid content-start gap-2">
                    <Label htmlFor="gender" className="text-sm text-white/80">Gender</Label>
                    <Select value={form.gender} onValueChange={(value) => update('gender', value ?? 'unknown')}>
                      <SelectTrigger id="gender" className="h-10 w-full border-white/10 bg-black/35 text-white">
                        <SelectValue placeholder="Select gender" />
                      </SelectTrigger>
                      <SelectContent className="border-white/10 bg-[#0b1116] text-white">
                        <SelectItem value="unknown">Unknown</SelectItem>
                        <SelectItem value="female">Female</SelectItem>
                        <SelectItem value="male">Male</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <DateField
                    id="date-of-birth"
                    label="Date of birth"
                    value={form.dateOfBirth}
                    onChange={(value) => update('dateOfBirth', value)}
                    maxDate={latestAdultBirthDate}
                    required
                  />
                  <TextField
                    id="photo-url"
                    label="Photo URL or path"
                    value={form.photoUrl}
                    onChange={(value) => update('photoUrl', value)}
                    maxLength={2000}
                    placeholder="https://… or a stored image path"
                    helper="Optional. The backend stores this as a text path."
                  />
                  <div className="flex min-h-10 items-center gap-3 rounded-lg border border-white/[0.07] bg-black/20 px-3 py-2 max-[700px]:col-span-1 min-[701px]:col-span-2">
                    <Checkbox
                      id="criminal-record"
                      checked={form.criminalRecord}
                      onCheckedChange={(checked) => update('criminalRecord', checked === true)}
                      className="border-white/25 data-checked:border-cyan-200 data-checked:bg-cyan-200 data-checked:text-black"
                    />
                    <Label htmlFor="criminal-record" className="cursor-pointer text-sm text-white/75">
                      Criminal record recorded
                    </Label>
                  </div>
                </div>
              </section>

              <Separator className="bg-white/[0.08]" />

              <section className="grid gap-4" aria-labelledby="journey-section-title">
                <SectionHeading id="journey-section-title" title="Airport journey" description="The checkpoint and planned exit details for this active journey." />
                <div className="grid grid-cols-2 gap-x-5 gap-y-5 max-[700px]:grid-cols-1">
                  <div className="grid content-start gap-2 min-[701px]:col-span-2">
                    <TextField
                      id="entry-checkpoint-id"
                      label="Airport entry checkpoint ID"
                      value={form.entryCheckpointId}
                      onChange={(value) => update('entryCheckpointId', value)}
                      required
                      placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                      helper="Use the UUID of an active checkpoint marked as an entry point. The backend currently has no checkpoint-list endpoint."
                    />
                  </div>
                  <TextField
                    id="occupation"
                    label="Occupation"
                    value={form.occupation}
                    onChange={(value) => update('occupation', value)}
                    minLength={2}
                    maxLength={50}
                    required
                    placeholder="Occupation"
                    helper="Also used as the permit occupation in the current API."
                  />
                  <DateTimeField
                    id="expected-exit"
                    label="Expected exit"
                    value={form.expectedExitDate}
                    onChange={(value) => update('expectedExitDate', value)}
                    time={form.expectedExitTime}
                    onTimeChange={(value) => update('expectedExitTime', value)}
                    required
                  />
                  <TextareaField
                    id="declared-states"
                    label="Declared states"
                    value={form.declaredStates}
                    onChange={(value) => update('declaredStates', value)}
                    helper="Optional. Separate multiple states with commas or new lines."
                  />
                </div>
              </section>

              <Separator className="bg-white/[0.08]" />

              <section className="grid gap-4" aria-labelledby="visa-section-title">
                <SectionHeading id="visa-section-title" title="Visa and permit" description="Visa data and the permit validity period for this journey." />
                <div className="grid grid-cols-2 gap-x-5 gap-y-5 max-[700px]:grid-cols-1">
                  <TextField
                    id="visa-type"
                    label="Visa type"
                    value={form.visaType}
                    onChange={(value) => update('visaType', value)}
                    minLength={2}
                    maxLength={100}
                    required
                    placeholder="Visa type"
                  />
                  <TextField
                    id="visa-number"
                    label="Visa number"
                    value={form.visaNumber}
                    onChange={(value) => update('visaNumber', value)}
                    maxLength={100}
                    placeholder="Optional"
                  />
                  <TextField
                    id="permit-type"
                    label="Permit type"
                    value={form.permitType}
                    onChange={(value) => update('permitType', value)}
                    maxLength={200}
                    placeholder="ILP, RAP, tourist visa, etc."
                  />
                  <TextField
                    id="permit-issued-by"
                    label="Permit issued by"
                    value={form.permitIssuedBy}
                    onChange={(value) => update('permitIssuedBy', value)}
                    maxLength={255}
                    placeholder="Issuing authority"
                  />
                  <DateTimeField
                    id="permit-valid-from"
                    label="Permit valid from"
                    value={form.permitValidFromDate}
                    onChange={(value) => update('permitValidFromDate', value)}
                    time={form.permitValidFromTime}
                    onTimeChange={(value) => update('permitValidFromTime', value)}
                    required
                  />
                  <DateTimeField
                    id="permit-valid-to"
                    label="Permit valid to"
                    value={form.permitValidToDate}
                    onChange={(value) => update('permitValidToDate', value)}
                    time={form.permitValidToTime}
                    onTimeChange={(value) => update('permitValidToTime', value)}
                    required
                  />
                  <TextareaField
                    id="permit-permitted-states"
                    label="Permit permitted states"
                    value={form.permitPermittedStates}
                    onChange={(value) => update('permitPermittedStates', value)}
                    helper="Optional. Separate multiple states with commas or new lines."
                  />
                </div>
              </section>

              {(error || success) && (
                <div
                  role={error ? 'alert' : 'status'}
                  className={`flex items-start gap-3 rounded-lg border px-4 py-3 text-sm ${error ? 'border-rose-300/20 bg-rose-300/[0.06] text-rose-100' : 'border-emerald-300/20 bg-emerald-300/[0.06] text-emerald-100'}`}
                >
                  {error ? <AlertTriangle className="mt-0.5 size-4 shrink-0" /> : <BadgeCheck className="mt-0.5 size-4 shrink-0" />}
                  <span>{error || success}</span>
                </div>
              )}

              <div className="flex items-center justify-between gap-4 border-t border-white/[0.07] pt-5 max-[600px]:flex-col-reverse max-[600px]:items-stretch">
                <p className="max-w-lg text-xs leading-relaxed text-white/40">
                  Submitting creates or updates the traveler record and opens an active journey through the existing registration API.
                </p>
                <Button
                  type="submit"
                  disabled={submitting}
                  className="h-11 min-w-48 bg-cyan-100 px-5 font-semibold text-[#071014] hover:bg-cyan-50"
                >
                  {submitting ? 'Registering…' : 'Register traveler'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}

function SectionHeading({ id, title, description }: { id: string; title: string; description: string }) {
  return (
    <div>
      <h2 id={id} className="text-sm font-semibold tracking-wide text-white">{title}</h2>
      <p className="mt-1 text-xs text-white/45">{description}</p>
    </div>
  )
}

function TextareaField({
  id,
  label,
  value,
  onChange,
  helper,
}: {
  id: string
  label: string
  value: string
  onChange: (value: string) => void
  helper: string
}) {
  return (
    <div className="grid content-start gap-2">
      <Label htmlFor={id} className="text-sm text-white/80">{label}</Label>
      <Textarea
        id={id}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        rows={2}
        placeholder="Optional"
        className="min-h-20 resize-y border-white/10 bg-black/35 text-white placeholder:text-white/30"
      />
      <p className="text-xs leading-relaxed text-white/45">{helper}</p>
    </div>
  )
}
