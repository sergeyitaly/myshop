import { SVGProps } from "react"
import { CartIcon } from "./CartIcon"
import { CrossSign } from "./CrossSign"

interface AppIconProps extends SVGProps<SVGSVGElement> {
    iconName: 'cart' | 'cross'

}

export const AppIcon = ({iconName, ...props}: AppIconProps) => {
    
    switch (iconName){
        case 'cart': return <CartIcon {...props}/>
        case 'cross': return <CrossSign {...props}/>
        default: return <CartIcon {...props}/>
    }
}