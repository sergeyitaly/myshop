import { SVGProps } from "react"
import { CartIcon } from "./CartIcon"
import { CrossSign } from "./CrossSign"
import { VaseIcon } from "./VaseIcon"

interface AppIconProps extends SVGProps<SVGSVGElement> {
    iconName: 'cart' | 'cross' | 'vase'

}

export const AppIcon = ({iconName, ...props}: AppIconProps) => {
    
    switch (iconName){
        case 'cart': return <CartIcon {...props}/>
        case 'cross': return <CrossSign {...props}/>
        case 'vase': return <VaseIcon {...props}/>
        default: return <CartIcon {...props}/>
    }
}