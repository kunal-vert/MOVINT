import { lazy, Suspense } from 'react'
import Navbar from './components/common/Navbar'
import { Navigate, Route, Routes } from 'react-router-dom'
import deploymentPoints from './components/deployment/deploymentPoints'

const PageNotFound = lazy(() => import('./components/common/PageNotFound'))
const RoutePreview = lazy(() => import('./components/common/RoutePreview'))
const UiDeployment = lazy(() => import('./components/deployment/UiDeployment'))
const EdenSignIn = lazy(() => import('./components/auth/EdenSignIn'))
const TravelerForm = lazy(() => import('./components/immigration/TravelerForm'))
const Alerts = lazy(() => import('./pages/Alerts'))
const Geomap = lazy(() => import('./pages/Geomap'))
const Tracking = lazy(() => import('./pages/Tracking'))

export default function App() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-black" aria-busy="true" />}>
      <Routes>
        <Route path="/login" element={<EdenSignIn />} />
        <Route
          path="/*"
          element={
            <div className="dark flex min-h-screen flex-col bg-black px-8 pt-5.5 max-[600px]:px-3.5 max-[600px]:pt-3.5">
              <Navbar />
              <Routes>
                <Route path="/" element={<Navigate to="/tracking" replace />} />
                <Route path="/tracking" element={<Tracking />} />
                <Route path="/alerts" element={<Alerts />} />
                <Route path="/geomap" element={<Geomap />} />
                <Route path="/deployment" element={<UiDeployment />}>
                  {deploymentPoints.map(({ label, path }) => (
                    <Route
                      key={path}
                      path={path}
                      element={
                        path === 'airport' ? (
                          <TravelerForm />
                        ) : (
                          <RoutePreview fileName={label} />
                        )
                      }
                    />
                  ))}
                </Route>
                <Route path="*" element={<PageNotFound />} />
              </Routes>
            </div>
          }
        />
      </Routes>
    </Suspense>
  )
}
