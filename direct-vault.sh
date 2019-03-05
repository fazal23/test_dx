#!/bin/bash
export VAULT_ADDR=URL OF VAULT
export VAULT_SKIP_VERIFY=true
/vault login -address=URL OF VAULT token="$RTOKEN"
/vault policy write $POLICYCOMMITERNAME $WORKSPACE/policies/$POLICYNAME 
