import { SVGProps } from "react"
import { CartIcon } from "./CartIcon"
import { CrossSign } from "./CrossSign"
import { VaseIcon } from "./VaseIcon"
import DeleteIcon from '@mui/icons-material/Delete';
import { AppIconNames } from "../../constants";

interface AppIconProps extends SVGProps<SVGSVGElement> {
    iconName: AppIconNames
}

export const AppIcon = ({iconName, ...props}: AppIconProps) => {
    
    switch (iconName){
        case 'cart': return <CartIcon {...props}/>
        case 'cross': return <CrossSign {...props}/>
        case 'vase': return <VaseIcon {...props}/>
        case 'delete': return <DeleteIcon />
        default: return <CartIcon {...props}/>
    }
}