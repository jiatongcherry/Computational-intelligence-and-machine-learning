import { formatCurrency } from "../scripts/utils/money.js";

if (formatCurrency(2095) === "20.95"){
    console.log("test passed");
} else {
    console.log("test failed");
}
