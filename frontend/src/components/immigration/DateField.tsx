import { useState } from 'react'
import { CalendarDays } from 'lucide-react'
import { Button } from '@/components/shadcn/button'
import { Calendar } from '@/components/shadcn/calendar'
import { Label } from '@/components/shadcn/label'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/shadcn/popover'
import { Input } from '@/components/shadcn/input'

interface DateFieldProps {
  id: string
  label: string
  value: string
  onChange: (value: string) => void
  maxDate?: Date
  required?: boolean
  showLabel?: boolean
}

interface DateTimeFieldProps extends DateFieldProps {
  time: string
  onTimeChange: (value: string) => void
}

function asLocalDate(value: string) {
  if (!value) return undefined
  const [year, month, day] = value.split('-').map(Number)
  return new Date(year, month - 1, day, 12)
}

function asDateValue(value: Date) {
  const year = value.getFullYear()
  const month = String(value.getMonth() + 1).padStart(2, '0')
  const day = String(value.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function DateField({
  id,
  label,
  value,
  onChange,
  maxDate,
  required = false,
  showLabel = true,
}: DateFieldProps) {
  const [open, setOpen] = useState(false)
  const selectedDate = asLocalDate(value)
  const displayValue = selectedDate
    ? new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(selectedDate)
    : 'Choose a date'

  return (
    <div className="grid gap-2">
      {showLabel && (
        <Label htmlFor={id} className="text-sm text-white/80">
          {label}{required ? ' *' : ''}
        </Label>
      )}
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger
          render={
            <Button
              id={id}
              type="button"
              variant="outline"
              aria-required={required}
              className="h-10 w-full justify-start border-white/10 bg-black/35 px-3 text-left font-normal text-white hover:bg-white/[0.07] hover:text-white"
            />
          }
        >
          <CalendarDays className="mr-2 size-4 text-cyan-200/80" />
          <span className={selectedDate ? '' : 'text-white/45'}>{displayValue}</span>
        </PopoverTrigger>
        <PopoverContent
          align="start"
          className="w-auto border-white/10 bg-[#0b1116] p-2 text-white"
        >
          <Calendar
            mode="single"
            selected={selectedDate}
            onSelect={(date) => {
              if (date) onChange(asDateValue(date))
              setOpen(false)
            }}
            disabled={maxDate ? { after: maxDate } : undefined}
            captionLayout="dropdown"
            startMonth={maxDate ? new Date(maxDate.getFullYear() - 100, 0, 1) : undefined}
            endMonth={maxDate}
            className="[--cell-size:--spacing(9)]"
          />
        </PopoverContent>
      </Popover>
    </div>
  )
}

export function DateTimeField({
  id,
  label,
  value,
  onChange,
  time,
  onTimeChange,
  required = false,
}: DateTimeFieldProps) {
  return (
    <div className="grid gap-2">
      <Label htmlFor={`${id}-date`} className="text-sm text-white/80">
        {label}{required ? ' *' : ''}
      </Label>
      <div className="grid grid-cols-[minmax(0,1fr)_116px] gap-2">
        <DateField
          id={`${id}-date`}
          label={label}
          value={value}
          onChange={onChange}
          showLabel={false}
        />
        <div className="grid gap-2">
          <Label htmlFor={`${id}-time`} className="sr-only">
            {label} time
          </Label>
          <Input
            id={`${id}-time`}
            type="time"
            required={required}
            value={time}
            onChange={(event) => onTimeChange(event.target.value)}
            className="h-10 border-white/10 bg-black/35 text-white [color-scheme:dark]"
          />
        </div>
      </div>
    </div>
  )
}

export default DateField
