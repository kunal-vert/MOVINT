interface RoutePreviewProps {
  fileName: string
}

export default function RoutePreview({ fileName }: RoutePreviewProps) {
  return (
    <main className="grid flex-1 place-items-center text-center">
      <h1 className="text-5xl font-bold tracking-wide text-white max-[600px]:text-4xl">
        {fileName}
      </h1>
    </main>
  )
}
