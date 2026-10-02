import { Outlet } from 'react-router-dom'
import DeploymentLayout from './DeploymentLayout'

export default function UiDeployment() {
  return (
    <DeploymentLayout>
      <Outlet />
    </DeploymentLayout>
  )
}
