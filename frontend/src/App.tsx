import Navbar from './components/common/Navbar'
import { Navigate, Route, Routes } from 'react-router-dom'
import PageNotFound from './components/common/PageNotFound'
import Alerts from './pages/Alerts'
import Deployment from './pages/Deployment'
import UiDeployment from './components/deployment/UiDeployment'
import deploymentPoints from './components/deployment/deploymentPoints'
import RoutePreview from './components/common/RoutePreview'
import Geomap from './pages/Geomap'
import Tracking from './pages/Tracking'

export default function App() {
  return (
    <div className="flex min-h-screen flex-col bg-black px-8 pt-[22px] max-[600px]:px-[14px] max-[600px]:pt-[14px]">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/tracking" replace />} />
        <Route path="/tracking" element={<Tracking />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/geomap" element={<Geomap />} />
        <Route path="/deployment" element={<UiDeployment />}>
          <Route index element={<Deployment />} />
          {deploymentPoints.map(({ label, path }) => (
            <Route key={path} path={path} element={<RoutePreview fileName={label} />} />
          ))}
        </Route>
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </div>
  )
}
