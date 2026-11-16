targetScope = 'resourceGroup'

@description('A short name unique within the shared course resource group, for example x11-p01.')
@minLength(3)
@maxLength(30)
param vmName string

param location string = resourceGroup().location

@description('Validate regional availability, policy and quota before the course.')
param vmSize string = 'Standard_D2s_v6'

@description('Public IPv4 address of the course network or participant, without a CIDR suffix. SSH is limited to this /32.')
@minLength(7)
@maxLength(15)
param sshSourceIpv4 string

@secure()
@description('Strong generated bootstrap password for NEW VM provisioning. Set the temporary course password after bootstrap.')
param adminPassword string

param adminUsername string = 'course'

@description('Use the exact Marketplace image version from the rehearsal for the second-machine check.')
param imageVersion string = 'latest'

var tags = {
  exercise: 'x11'
  participant: vmName
}

resource nsg 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: '${vmName}-nsg'
  location: location
  tags: tags
  properties: {
    securityRules: [
      {
        name: 'SSH-from-course-network'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '${sshSourceIpv4}/32'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '22'
        }
      }
      {
        name: 'Deny-other-inbound'
        properties: {
          priority: 200
          direction: 'Inbound'
          access: 'Deny'
          protocol: '*'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
        }
      }
    ]
  }
}

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: '${vmName}-vnet'
  location: location
  tags: tags
  properties: {
    addressSpace: { addressPrefixes: ['10.11.0.0/24'] }
    subnets: [
      {
        name: 'agents'
        properties: {
          addressPrefix: '10.11.0.0/24'
          networkSecurityGroup: { id: nsg.id }
        }
      }
    ]
  }
}

resource publicIp 'Microsoft.Network/publicIPAddresses@2024-05-01' = {
  name: '${vmName}-ip'
  location: location
  tags: tags
  sku: { name: 'Standard' }
  properties: { publicIPAllocationMethod: 'Static' }
}

resource nic 'Microsoft.Network/networkInterfaces@2024-05-01' = {
  name: '${vmName}-nic'
  location: location
  tags: tags
  properties: {
    ipConfigurations: [
      {
        name: 'primary'
        properties: {
          privateIPAllocationMethod: 'Dynamic'
          publicIPAddress: { id: publicIp.id }
          subnet: { id: '${vnet.id}/subnets/agents' }
        }
      }
    ]
  }
}

resource vm 'Microsoft.Compute/virtualMachines@2024-07-01' = {
  name: vmName
  location: location
  tags: tags
  properties: {
    hardwareProfile: { vmSize: vmSize }
    storageProfile: {
      imageReference: {
        publisher: 'Canonical'
        offer: 'ubuntu-24_04-lts'
        sku: 'server'
        version: imageVersion
      }
      osDisk: {
        createOption: 'FromImage'
        deleteOption: 'Delete'
        diskSizeGB: 64
        managedDisk: { storageAccountType: 'StandardSSD_LRS' }
      }
    }
    osProfile: {
      computerName: vmName
      adminUsername: adminUsername
      adminPassword: adminPassword
      customData: base64(loadTextContent('cloud-init.yaml'))
      linuxConfiguration: {
        disablePasswordAuthentication: false
        provisionVMAgent: true
      }
    }
    securityProfile: {
      securityType: 'TrustedLaunch'
      uefiSettings: {
        secureBootEnabled: true
        vTpmEnabled: true
      }
    }
    networkProfile: {
      networkInterfaces: [{ id: nic.id }]
    }
  }
}

output publicIpAddress string = publicIp.properties.ipAddress
output vmResourceId string = vm.id
